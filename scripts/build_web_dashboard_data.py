"""Create a compact JSON bundle for the static GitHub Pages dashboard."""

from pathlib import Path
import json

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed" / "dashboard"
OUTPUT = ROOT / "E-commerence analysis" / "dashboard_data.json"


def build() -> None:
    fact = pd.read_csv(DATA / "fact_amazon_sales.csv", low_memory=False)
    fact["date"] = pd.to_datetime(fact["date"], errors="coerce")
    fact["amount"] = pd.to_numeric(fact["amount"], errors="coerce")
    fact["qty"] = pd.to_numeric(fact["qty"], errors="coerce")

    order_status = pd.read_csv(DATA / "dim_order_status.csv", low_memory=False)
    order_status["order_date"] = pd.to_datetime(order_status["order_date"], errors="coerce")
    international = pd.read_csv(DATA / "fact_international_sales.csv", low_memory=False)
    international["date"] = pd.to_datetime(international["date"], errors="coerce")

    delivered = fact[fact["is_delivered_status_proxy"].eq(True)]
    valid_price = delivered[delivered["amount"].notna() & delivered["qty"].gt(0)].copy()
    valid_price["unit_price"] = valid_price["amount"] / valid_price["qty"]

    def records(frame: pd.DataFrame) -> list[dict]:
        return json.loads(frame.to_json(orient="records", date_format="iso"))

    monthly = (
        fact.groupby(["month_label", "is_partial_period"], dropna=False)
        .agg(
            reported_amount=("amount", "sum"),
            gross_units=("qty", "sum"),
            lines=("order_id", "size"),
            distinct_orders=("order_id", "nunique"),
            amount_coverage=("amount", lambda values: values.notna().mean()),
        )
        .reset_index()
    )
    monthly["month_order"] = pd.to_datetime(monthly["month_label"], format="%b %Y")
    monthly = monthly.sort_values("month_order").drop(columns="month_order")

    category = (
        fact.groupby("category", dropna=False)
        .agg(reported_amount=("amount", "sum"), gross_units=("qty", "sum"), distinct_orders=("order_id", "nunique"))
        .reset_index()
        .sort_values("reported_amount", ascending=False)
    )
    category["contribution"] = category["reported_amount"] / category["reported_amount"].sum()

    sku = (
        fact.groupby("sku", dropna=False)
        .agg(reported_amount=("amount", "sum"), gross_units=("qty", "sum"), distinct_orders=("order_id", "nunique"))
        .reset_index()
        .sort_values("reported_amount", ascending=False)
        .head(10)
    )
    sku["contribution"] = sku["reported_amount"] / fact["amount"].sum()

    price_bands = (
        valid_price.groupby("reported_unit_price_band", observed=False)
        .agg(reported_amount=("amount", "sum"), gross_units=("qty", "sum"), lines=("amount", "size"))
        .reset_index()
    )
    price_bands["reported_unit_price_band"] = price_bands["reported_unit_price_band"].astype(str)

    category_price = (
        valid_price.groupby("category", dropna=False)
        .agg(reported_unit_price_proxy=("unit_price", "mean"), valid_lines=("unit_price", "size"))
        .reset_index()
        .sort_values("reported_unit_price_proxy", ascending=False)
    )

    b2b = (
        fact.groupby("b2b", dropna=False)
        .agg(reported_amount=("amount", "sum"), gross_units=("qty", "sum"), distinct_orders=("order_id", "nunique"))
        .reset_index()
    )
    b2b["label"] = b2b["b2b"].map({True: "B2B", False: "B2C"}).fillna("Unknown")

    statuses = (
        order_status.groupby("status_label", dropna=False)
        .agg(distinct_orders=("order_id", "nunique"))
        .reset_index()
        .sort_values("distinct_orders", ascending=False)
    )
    statuses["composition"] = statuses["distinct_orders"] / order_status["order_id"].nunique()

    state = (
        fact.groupby("ship_state", dropna=False)
        .agg(reported_amount=("amount", "sum"), distinct_orders=("order_id", "nunique"))
        .reset_index()
        .sort_values("reported_amount", ascending=False)
        .head(10)
    )

    payload = {
        "scope": {
            "amazon_lines": int(len(fact)),
            "amazon_orders": int(fact["order_id"].nunique()),
            "reported_amount": float(fact["amount"].sum()),
            "amount_coverage": float(fact["amount"].notna().mean()),
            "gross_units": float(fact["qty"].sum()),
            "international_lines": int(len(international)),
            "international_reported_amount": float(international["reported_gross_amount"].sum()),
            "international_pieces": float(international["pieces"].sum()),
            "delivered_proxy_orders": int(order_status["has_delivered_status_proxy"].sum()),
            "valid_price_lines": int(len(valid_price)),
            "mixed_status_orders": int(order_status["mixed_status_flag"].sum()),
            "date_range": [fact["date"].min().strftime("%Y-%m-%d"), fact["date"].max().strftime("%Y-%m-%d")],
        },
        "monthly": records(monthly),
        "category": records(category),
        "sku": records(sku),
        "price_bands": records(price_bands),
        "category_price": records(category_price),
        "b2b": records(b2b),
        "statuses": records(statuses),
        "states": records(state),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
