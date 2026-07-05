from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
CLEAN_DIR = ROOT / "data" / "cleaned"
REPORT_DIR = ROOT / "reports"


NUMERIC_HINTS = (
    "amount",
    "amt",
    "qty",
    "pcs",
    "rate",
    "stock",
    "weight",
    "mrp",
    "price",
    "tp",
)
DATE_HINTS = ("date",)
ID_TEXT_HINTS = ("id", "sku", "asin", "code", "postal", "pincode")


def snake_case(name: object) -> str:
    text = str(name).strip().lower()
    text = text.replace("&", " and ")
    text = re.sub(r"[^0-9a-zA-Z]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "unnamed"


def clean_text_value(value: object) -> object:
    if pd.isna(value):
        return pd.NA
    if isinstance(value, str):
        value = value.strip()
        value = re.sub(r"\s+", " ", value)
        if value == "" or value.lower() in {"nan", "none", "null", "na", "n/a", "-"}:
            return pd.NA
    return value


def to_number(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype("string")
        .str.replace(r"[₹$,]", "", regex=True)
        .str.replace(r"^\((.*)\)$", r"-\1", regex=True)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")


def parse_date_series(series: pd.Series) -> pd.Series:
    parsed = pd.to_datetime(series, errors="coerce", dayfirst=False)
    if parsed.notna().sum() == 0:
        parsed = pd.to_datetime(series, errors="coerce", dayfirst=True)
    return parsed.dt.strftime("%Y-%m-%d").astype("string")


def read_csv(path: Path, nrows: int | None = None) -> pd.DataFrame:
    return pd.read_csv(path, dtype="object", encoding="utf-8", encoding_errors="replace", nrows=nrows)


def drop_index_like_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in list(df.columns):
        if col == "index":
            numeric = pd.to_numeric(df[col], errors="coerce")
            if numeric.notna().all() and (numeric.reset_index(drop=True) == pd.RangeIndex(len(df))).all():
                df = df.drop(columns=[col])
    return df


def profile_frame(
    file_name: str,
    raw_df: pd.DataFrame,
    cleaned_df: pd.DataFrame,
    notes: list[str],
    duplicate_rows_removed: int,
) -> dict:
    missing = cleaned_df.isna().sum().sort_values(ascending=False)
    missing_rows = [
        {
            "column": col,
            "missing_count": int(count),
            "missing_pct": round(float(count) / len(cleaned_df) * 100, 2) if len(cleaned_df) else 0,
        }
        for col, count in missing.items()
        if int(count) > 0
    ]
    numeric_cols = [
        col
        for col in cleaned_df.columns
        if any(hint in col for hint in NUMERIC_HINTS) and not any(id_hint in col for id_hint in ID_TEXT_HINTS)
    ]
    negative_values = {
        col: int((pd.to_numeric(cleaned_df[col], errors="coerce") < 0).sum())
        for col in numeric_cols
        if col in cleaned_df.columns
    }
    return {
        "file": file_name,
        "raw_rows": int(len(raw_df)),
        "raw_columns": int(raw_df.shape[1]),
        "cleaned_rows": int(len(cleaned_df)),
        "cleaned_columns": int(cleaned_df.shape[1]),
        "exact_duplicate_rows_removed": int(duplicate_rows_removed),
        "missing_values": missing_rows[:25],
        "negative_values": {k: v for k, v in negative_values.items() if v > 0},
        "columns": list(cleaned_df.columns),
        "notes": notes,
    }


def standard_clean(path: Path) -> tuple[pd.DataFrame, dict]:
    raw_df = read_csv(path)
    df = raw_df.copy()
    notes: list[str] = []

    df.columns = [snake_case(col) for col in df.columns]
    before_cols = set(df.columns)
    df = df.dropna(axis=1, how="all")
    dropped_all_null = sorted(before_cols - set(df.columns))
    if dropped_all_null:
        notes.append(f"Dropped all-null columns: {', '.join(dropped_all_null)}.")

    df = drop_index_like_columns(df)
    if "index" not in df.columns and "index" in before_cols:
        notes.append("Dropped generated index column.")

    for col in list(df.columns):
        if col.startswith("unnamed"):
            non_null = df[col].dropna().astype(str).str.strip().str.lower().unique()
            if len(non_null) == 0 or set(non_null).issubset({"false"}):
                df = df.drop(columns=[col])
                notes.append(f"Dropped parser artifact column `{col}`.")

    for col in df.columns:
        df[col] = df[col].map(clean_text_value)

    before_rows = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    removed = before_rows - len(df)
    if removed:
        notes.append(f"Removed {removed:,} exact duplicate rows.")

    for col in list(df.columns):
        lower = col.lower()
        if any(id_hint in lower for id_hint in ID_TEXT_HINTS):
            df[col] = df[col].astype("string")
        elif any(hint in lower for hint in NUMERIC_HINTS):
            converted = to_number(df[col])
            if converted.notna().sum() >= max(1, int(df[col].notna().sum() * 0.7)):
                df[col] = converted
        elif any(hint in lower for hint in DATE_HINTS):
            parsed = parse_date_series(df[col])
            if parsed.notna().sum() >= max(1, int(df[col].notna().sum() * 0.7)):
                df[col] = parsed

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("string")

    return df, profile_frame(path.name, raw_df, df, notes, removed)


def clean_warehouse(path: Path) -> tuple[pd.DataFrame, dict]:
    raw_df = read_csv(path)
    df = raw_df.copy()
    df.columns = [snake_case(col) for col in df.columns]
    df = drop_index_like_columns(df)
    df = df.rename(
        columns={
            "shiprocket": "cost_head",
            "unnamed_1": "shiprocket_price_per_unit",
            "increff": "increff_price_per_unit",
        }
    )
    df = df.iloc[1:].reset_index(drop=True)
    for col in df.columns:
        df[col] = df[col].map(clean_text_value)
    for col in ["shiprocket_price_per_unit", "increff_price_per_unit"]:
        df[col] = to_number(df[col])
    df = df.dropna(subset=["shiprocket_price_per_unit", "increff_price_per_unit"], how="all")
    before_rows = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    removed = before_rows - len(df)
    notes = [
        "Promoted embedded first row to semantic column names.",
        "Converted rupee-denominated per-unit prices to numeric values.",
        "Removed narrative section headings without comparable price values.",
    ]
    return df, profile_frame(path.name, raw_df, df, notes, removed)


def clean_expense(path: Path) -> tuple[pd.DataFrame, dict]:
    raw_df = read_csv(path)
    df = raw_df.copy()
    df.columns = [snake_case(col) for col in df.columns]
    df = drop_index_like_columns(df)
    df = df.iloc[1:].reset_index(drop=True)

    receipts = df[["recived_amount", "unnamed_1"]].rename(
        columns={"recived_amount": "particular", "unnamed_1": "amount"}
    )
    receipts["transaction_type"] = "received_amount"
    expenses = df[["expance", "unnamed_3"]].rename(columns={"expance": "particular", "unnamed_3": "amount"})
    expenses["transaction_type"] = "expense"
    long_df = pd.concat([receipts, expenses], ignore_index=True)
    long_df = long_df[["transaction_type", "particular", "amount"]]

    for col in long_df.columns:
        long_df[col] = long_df[col].map(clean_text_value)
    long_df["amount"] = to_number(long_df["amount"])
    long_df = long_df.dropna(subset=["particular", "amount"], how="all")
    missing_particular = long_df["particular"].isna() & long_df["amount"].notna()
    long_df.loc[missing_particular, "particular"] = np.where(
        long_df.loc[missing_particular, "transaction_type"].eq("expense"),
        "Unlabelled expense total/balance",
        "Unlabelled received total/balance",
    )
    long_df["record_type"] = np.where(
        long_df["particular"].astype("string").str.lower().str.contains("total|pending|balance", na=False),
        "summary",
        "detail",
    )
    long_df = long_df[["transaction_type", "record_type", "particular", "amount"]]
    before_rows = len(long_df)
    long_df = long_df.drop_duplicates().reset_index(drop=True)
    removed = before_rows - len(long_df)
    notes = [
        "Reshaped two side-by-side receipt and expense sections into one auditable long table.",
        "Flagged totals, pending amount, and unlabelled balance rows as summary records.",
        "Kept original spelling in source notes; standardized output column names.",
    ]
    return long_df, profile_frame(path.name, raw_df, long_df, notes, removed)


SPECIAL_CLEANERS = {
    "Cloud Warehouse Compersion Chart.csv": clean_warehouse,
    "Expense IIGF.csv": clean_expense,
}


def write_markdown_report(profiles: list[dict]) -> None:
    lines: list[str] = [
        "# E-Commerce Data Quality & Cleaning Report",
        "",
        "## Cleaning Rules Applied",
        "",
        "- Preserved raw files under `data/raw` and wrote cleaned files under `data/cleaned`.",
        "- Standardized column names to lowercase snake_case.",
        "- Removed generated index columns and fully empty columns.",
        "- Trimmed whitespace, normalized blank-like values to missing, and removed exact duplicate rows.",
        "- Converted numeric amount, price, quantity, rate, MRP, stock, and weight fields to numeric values where safe.",
        "- Converted date fields to ISO `YYYY-MM-DD` where safe.",
        "- Treated SKU, ASIN, order IDs, codes, and postal codes as text identifiers.",
        "- Reshaped special report-style CSVs into analysis-ready tables.",
        "",
        "## File-Level Summary",
        "",
        "| File | Raw Rows | Cleaned Rows | Raw Columns | Cleaned Columns | Duplicate Rows Removed | Key Notes |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for p in profiles:
        notes = " ".join(p["notes"]) if p["notes"] else "Standard cleaning only."
        lines.append(
            f"| {p['file']} | {p['raw_rows']:,} | {p['cleaned_rows']:,} | "
            f"{p['raw_columns']:,} | {p['cleaned_columns']:,} | "
            f"{p['exact_duplicate_rows_removed']:,} | {notes} |"
        )

    lines.extend(["", "## Missing Value Highlights", ""])
    for p in profiles:
        lines.append(f"### {p['file']}")
        if not p["missing_values"]:
            lines.append("- No missing values after cleaning.")
        else:
            for item in p["missing_values"][:10]:
                lines.append(
                    f"- `{item['column']}`: {item['missing_count']:,} missing "
                    f"({item['missing_pct']}%)."
                )
        if p["negative_values"]:
            lines.append(f"- Negative numeric values detected: `{json.dumps(p['negative_values'])}`.")
        lines.append("")

    (REPORT_DIR / "data_quality_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    profiles: list[dict] = []
    for path in sorted(RAW_DIR.glob("*.csv")):
        cleaner = SPECIAL_CLEANERS.get(path.name, standard_clean)
        cleaned, profile = cleaner(path)
        output_name = f"{snake_case(path.stem)}_cleaned.csv"
        cleaned.to_csv(CLEAN_DIR / output_name, index=False)
        profile["cleaned_file"] = output_name
        profiles.append(profile)

    (REPORT_DIR / "data_quality_profile.json").write_text(
        json.dumps(profiles, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_markdown_report(profiles)

    print(json.dumps({"cleaned_files": len(profiles), "profiles": profiles}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
