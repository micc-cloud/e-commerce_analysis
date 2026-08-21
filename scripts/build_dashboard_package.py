"""Build Power BI-ready, source-local dashboard tables from cleaned CSVs."""

from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "cleaned"
OUTPUT = ROOT / "data" / "processed" / "dashboard"
sys.path.insert(0, str(ROOT))

from src.status_scope import add_status_scope


def date_key(values: pd.Series) -> pd.Series:
    return values.dt.strftime("%Y%m%d").astype("Int64")


def build() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)

    amazon = pd.read_csv(INPUT / "amazon_sale_report_cleaned.csv", low_memory=False)
    amazon["date"] = pd.to_datetime(amazon["date"], errors="coerce")
    amazon["amount"] = pd.to_numeric(amazon["amount"], errors="coerce")
    amazon["qty"] = pd.to_numeric(amazon["qty"], errors="coerce")
    amazon = add_status_scope(amazon)

    observed_dates = pd.Series(sorted(amazon["date"].dropna().unique()))
    min_date = observed_dates.min()
    max_date = observed_dates.max()
    month_start = observed_dates.dt.to_period("M").dt.to_timestamp()
    partial_months = {month_start.min(), month_start.max()}

    dim_date = pd.DataFrame({"date": observed_dates})
    dim_date["date_key"] = date_key(dim_date["date"])
    dim_date["year"] = dim_date["date"].dt.year
    dim_date["month_number"] = dim_date["date"].dt.month
    dim_date["month_start"] = dim_date["date"].dt.to_period("M").dt.to_timestamp()
    dim_date["month_label"] = dim_date["date"].dt.strftime("%b %Y")
    dim_date["is_partial_period"] = dim_date["month_start"].isin(partial_months)
    dim_date["observed_date_count_in_month"] = dim_date.groupby("month_start")["date"].transform("nunique")
    dim_date = dim_date.sort_values("date").reset_index(drop=True)
    dim_date.to_csv(OUTPUT / "dim_date.csv", index=False, date_format="%Y-%m-%d")

    fact = amazon.copy()
    fact["date_key"] = date_key(fact["date"])
    fact["month_start"] = fact["date"].dt.to_period("M").dt.to_timestamp()
    fact["month_label"] = fact["date"].dt.strftime("%b %Y")
    fact["is_partial_period"] = fact["month_start"].isin(partial_months)
    fact["amount_present"] = fact["amount"].notna()
    fact["reported_unit_price_proxy"] = np.where(
        fact["amount"].notna() & fact["qty"].gt(0),
        fact["amount"] / fact["qty"],
        np.nan,
    )
    fact["reported_unit_price_band"] = pd.cut(
        fact["reported_unit_price_proxy"],
        bins=[0, 500, 1000, 2000, np.inf],
        labels=["[0,500)", "[500,1000)", "[1000,2000)", "[2000,inf)"],
        right=False,
        include_lowest=True,
    ).astype("string")
    fact["b2b"] = fact["b2b"].astype("boolean")
    fact["is_cancelled_status_proxy"] = fact["status"].astype("string").str.lower().eq("cancelled")
    fact["is_return_status_proxy"] = fact["status"].astype("string").str.contains("return", case=False, na=False)
    fact["is_shipped_status_proxy"] = fact["status"].astype("string").str.lower().str.startswith("shipped", na=False)
    fact["is_delivered_status_proxy"] = fact["status"].eq("Shipped - Delivered to Buyer")

    fact_columns = [
        "order_id", "date", "date_key", "month_start", "month_label", "is_partial_period",
        "status", "status_group", "fulfilment", "sales_channel", "ship_service_level",
        "style", "sku", "category", "size", "asin", "courier_status", "qty", "currency",
        "amount", "amount_present", "reported_unit_price_proxy", "reported_unit_price_band", "ship_city", "ship_state",
        "ship_postal_code", "ship_country", "promotion_ids", "b2b", "fulfilled_by",
        "is_cancelled_status_proxy", "is_return_status_proxy", "is_shipped_status_proxy",
        "is_delivered_status_proxy",
    ]
    fact[fact_columns].to_csv(OUTPUT / "fact_amazon_sales.csv", index=False, date_format="%Y-%m-%d")

    dim_category = pd.DataFrame({"category": sorted(fact["category"].dropna().unique())})
    dim_category["category_key"] = dim_category["category"]
    dim_category = dim_category[["category_key", "category"]]
    dim_category.to_csv(OUTPUT / "dim_category.csv", index=False)

    dim_sku = (
        fact.sort_values(["sku", "date"])
        .groupby("sku", as_index=False)
        .agg(style=("style", "first"), category=("category", "first"), size=("size", "first"))
        .rename(columns={"sku": "sku_key"})
    )
    dim_sku["sku"] = dim_sku["sku_key"]
    dim_sku["mapping_scope"] = "Amazon source-local"
    dim_sku = dim_sku[["sku_key", "sku", "style", "category", "size", "mapping_scope"]]
    dim_sku.to_csv(OUTPUT / "dim_sku.csv", index=False)

    order_status = (
        fact.groupby("order_id", as_index=False)
        .agg(
            order_date=("date", "min"),
            status_values=("status", lambda values: tuple(sorted(values.dropna().unique()))),
            status_count=("status", "nunique"),
            has_cancelled_status_proxy=("is_cancelled_status_proxy", "any"),
            has_return_status_proxy=("is_return_status_proxy", "any"),
            has_shipped_status_proxy=("is_shipped_status_proxy", "any"),
            has_delivered_status_proxy=("is_delivered_status_proxy", "any"),
        )
    )
    order_status["status_label"] = np.where(
        order_status["status_count"].eq(1),
        order_status["status_values"].str[0],
        "MIXED_STATUS_REQUIRES_RULE",
    )
    order_status["mixed_status_flag"] = order_status["status_count"].gt(1)
    order_status["order_date_key"] = date_key(order_status["order_date"])
    order_status["status_values"] = order_status["status_values"].map(lambda values: " | ".join(values))
    order_status = order_status[
        [
            "order_id", "order_date", "order_date_key", "status_label", "status_values",
            "status_count", "mixed_status_flag", "has_cancelled_status_proxy",
            "has_return_status_proxy", "has_shipped_status_proxy", "has_delivered_status_proxy",
        ]
    ]
    order_status.to_csv(OUTPUT / "dim_order_status.csv", index=False, date_format="%Y-%m-%d")

    international = pd.read_csv(INPUT / "international_sale_report_cleaned.csv", low_memory=False)
    international["date"] = pd.to_datetime(international["date"], format="%m/%d/%Y", errors="coerce")
    international["date_key"] = date_key(international["date"])
    international["pieces"] = pd.to_numeric(international["pcs"], errors="coerce")
    international["reported_gross_amount"] = pd.to_numeric(international["gross_amt"], errors="coerce")
    international_fact = international[
        ["date", "date_key", "months", "style", "sku", "size", "pieces", "rate", "reported_gross_amount"]
    ]
    international_fact.to_csv(OUTPUT / "fact_international_sales.csv", index=False, date_format="%Y-%m-%d")

    print(f"Built dashboard package in {OUTPUT}")
    print(f"Amazon fact rows: {len(fact):,}; orders: {fact['order_id'].nunique():,}")
    print(f"International fact rows: {len(international_fact):,}; currency remains unspecified")


if __name__ == "__main__":
    build()
