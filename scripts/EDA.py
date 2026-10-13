"""Corrected Phase 2 EDA runner.

The notebook is the primary deliverable. This script keeps the same loading,
validation, aggregation, and report logic executable from the command line.
It deliberately separates Amazon and international sales scopes.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from src.visualizations import apply_business_style

DATA_DIR = REPO_ROOT / "data" / "cleaned"
OUTPUT_DIR = REPO_ROOT / "reports" / "eda_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_datasets() -> Dict[str, pd.DataFrame]:
    """Load all cleaned CSV files from the data directory."""
    datasets: Dict[str, pd.DataFrame] = {}
    for path in sorted(DATA_DIR.glob("*.csv")):
        datasets[path.stem] = pd.read_csv(path)
    return datasets


def summarize_dataset(name: str, df: pd.DataFrame) -> Dict[str, int]:
    """Create a lightweight data quality summary for each dataset."""
    return {
        "dataset": name,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_cells": int(df.isna().sum().sum()),
        "columns_with_missing_values": int((df.isna().sum() > 0).sum()),
    }


def main() -> None:
    """Run lightweight validation and save key summary tables."""
    apply_business_style()
    datasets = load_datasets()
    quality_summary = []
    for name, df in datasets.items():
        quality_summary.append(summarize_dataset(name, df))
    pd.DataFrame(quality_summary).to_csv(OUTPUT_DIR / "dataset_quality_summary.csv", index=False)
    amazon = datasets["amazon_sale_report_cleaned"]
    international = datasets["international_sale_report_cleaned"]
    amazon["date"] = pd.to_datetime(amazon["date"], format="%Y-%m-%d")
    international["date"] = pd.to_datetime(international["date"], format="%m/%d/%Y")
    amazon.groupby(amazon["date"].dt.to_period("M")).agg(amount=("amount", "sum"), orders=("order_id", "nunique"), units=("qty", "sum")).to_csv(OUTPUT_DIR / "amazon_monthly_summary.csv")
    international.groupby(international["date"].dt.to_period("M")).agg(gross_amt=("gross_amt", "sum"), pcs=("pcs", "sum")).to_csv(OUTPUT_DIR / "international_monthly_summary.csv")
    print(f"Validated {len(datasets)} cleaned datasets; summary tables written to {OUTPUT_DIR}.")


if __name__ == "__main__":
    main()
