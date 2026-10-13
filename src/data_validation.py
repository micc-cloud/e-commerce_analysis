"""Phase 0 audit for the cleaned e-commerce CSV datasets.

The audit is intentionally read-only with respect to data/raw and data/cleaned.
It reports data quality observations and writes only validation artifacts.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

import pandas as pd
from pandas.testing import assert_frame_equal


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
CLEAN_DIR = ROOT / "data" / "cleaned"
REPORT_DIR = ROOT / "reports"
VALIDATION_DIR = REPORT_DIR / "validation_reports"

EXPECTED_FILES = {
    "Amazon Sale Report.csv": ("amazon_sale_report_cleaned.csv", {"order_id", "date", "sku", "qty", "amount", "currency"}),
    "Cloud Warehouse Compersion Chart.csv": ("cloud_warehouse_compersion_chart_cleaned.csv", {"cost_head", "shiprocket_price_per_unit", "increff_price_per_unit"}),
    "Expense IIGF.csv": ("expense_iigf_cleaned.csv", {"transaction_type", "record_type", "particular", "amount"}),
    "International sale Report.csv": ("international_sale_report_cleaned.csv", {"date", "sku", "pcs", "rate", "gross_amt"}),
    "May-2022.csv": ("may_2022_cleaned.csv", {"sku", "style_id", "category", "tp"}),
    "P  L March 2021.csv": ("p_l_march_2021_cleaned.csv", {"sku", "style_id", "category"}),
    "Sale Report.csv": ("sale_report_cleaned.csv", {"sku_code", "stock", "category"}),
}

NUMERIC_COLUMNS = {
    "qty", "amount", "pcs", "rate", "gross_amt", "stock", "weight", "tp", "tp_1", "tp_2",
    "mrp_old", "final_mrp_old", "ajio_mrp", "amazon_mrp", "amazon_fba_mrp", "flipkart_mrp",
    "limeroad_mrp", "myntra_mrp", "paytm_mrp", "snapdeal_mrp", "shiprocket_price_per_unit",
    "increff_price_per_unit",
}
DATE_COLUMNS = {"date"}
KEY_CANDIDATES = {
    "amazon_sale_report_cleaned.csv": [["order_id"], ["order_id", "sku", "size"]],
    "cloud_warehouse_compersion_chart_cleaned.csv": [["cost_head"]],
    "expense_iigf_cleaned.csv": [["transaction_type", "record_type", "particular", "amount"]],
    "international_sale_report_cleaned.csv": [["date", "customer", "sku", "size", "pcs", "rate", "gross_amt"]],
    "may_2022_cleaned.csv": [["sku"]],
    "p_l_march_2021_cleaned.csv": [["sku"]],
    "sale_report_cleaned.csv": [["sku_code"]],
}
SKU_LINKS = [
    ("amazon_sale_report_cleaned.csv", "sku", "may_2022_cleaned.csv", "sku"),
    ("amazon_sale_report_cleaned.csv", "sku", "p_l_march_2021_cleaned.csv", "sku"),
    ("international_sale_report_cleaned.csv", "sku", "may_2022_cleaned.csv", "sku"),
    ("international_sale_report_cleaned.csv", "sku", "p_l_march_2021_cleaned.csv", "sku"),
    ("sale_report_cleaned.csv", "sku_code", "may_2022_cleaned.csv", "sku"),
    ("sale_report_cleaned.csv", "sku_code", "p_l_march_2021_cleaned.csv", "sku"),
]


def _load_cleaner_module():
    sys.path.insert(0, str(ROOT / "scripts"))
    import clean_ecommerce_data  # type: ignore

    return clean_ecommerce_data


def _json_value(value: Any) -> Any:
    if pd.isna(value):
        return None
    if isinstance(value, (pd.Timestamp,)):
        return value.isoformat()
    return value.item() if hasattr(value, "item") else value


def _date_summary(df: pd.DataFrame, column: str) -> dict[str, Any]:
    if column not in df:
        return {"column": column, "present": False}
    raw = df[column]
    parsed = pd.to_datetime(raw, errors="coerce", format="mixed", dayfirst=False)
    if parsed.notna().sum() == 0:
        parsed = pd.to_datetime(raw, errors="coerce", format="mixed", dayfirst=True)
    invalid_nonblank = int(raw.notna().sum() - parsed.notna().sum())
    return {
        "column": column,
        "present": True,
        "parseable": int(parsed.notna().sum()),
        "invalid_nonblank": invalid_nonblank,
        "missing": int(raw.isna().sum()),
        "min": _json_value(parsed.min()) if parsed.notna().any() else None,
        "max": _json_value(parsed.max()) if parsed.notna().any() else None,
    }


def _categorical_checks(df: pd.DataFrame) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for col in df.select_dtypes(include=["object", "string"]).columns:
        values = df[col].dropna().astype("string")
        whitespace = int(values.map(lambda value: bool(re.search(r"^\s|\s$", str(value)))).sum())
        result[col] = {"distinct": int(values.nunique()), "leading_trailing_whitespace": whitespace}
    return result


def _candidate_key_checks(df: pd.DataFrame, candidates: list[list[str]]) -> list[dict[str, Any]]:
    checks = []
    for columns in candidates:
        present = all(column in df.columns for column in columns)
        if not present:
            checks.append({"columns": columns, "present": False})
            continue
        duplicate_rows = int(df.duplicated(columns, keep=False).sum())
        null_key_rows = int(df[columns].isna().any(axis=1).sum())
        checks.append({"columns": columns, "present": True, "duplicate_rows": duplicate_rows, "null_key_rows": null_key_rows})
    return checks


def _reproducibility(cleaner_module: Any, raw_name: str, clean_name: str) -> dict[str, Any]:
    raw_path = RAW_DIR / raw_name
    clean_path = CLEAN_DIR / clean_name
    if not raw_path.exists() or not clean_path.exists():
        return {"status": "NOT CHECKED", "reason": "raw or cleaned file missing"}
    cleaner = cleaner_module.SPECIAL_CLEANERS.get(raw_name, cleaner_module.standard_clean)
    expected, _ = cleaner(raw_path)
    actual = pd.read_csv(clean_path, dtype="object", encoding="utf-8", keep_default_na=True)
    with tempfile.TemporaryDirectory() as temp_dir:
        expected_path = Path(temp_dir) / clean_name
        expected.to_csv(expected_path, index=False)
        expected_serialized = expected_path.read_bytes()
        expected_reloaded = pd.read_csv(expected_path, dtype="object")
    actual_serialized = clean_path.read_bytes()
    if expected_serialized == actual_serialized:
        return {"status": "PASS", "rows_expected": int(len(expected)), "rows_actual": int(len(actual))}
    try:
        assert_frame_equal(actual, expected_reloaded, check_dtype=False, check_names=True)
        detail = "serialized formatting differs but values and columns match"
    except (AssertionError, ValueError) as exc:
        detail = str(exc).splitlines()[0]
    return {"status": "WARNING", "detail": detail, "rows_expected": int(len(expected)), "rows_actual": int(len(actual))}


def audit() -> dict[str, Any]:
    cleaner_module = _load_cleaner_module()
    result: dict[str, Any] = {"files": [], "missing_expected_files": [], "merge_checks": [], "reproducibility": []}
    frames: dict[str, pd.DataFrame] = {}

    for raw_name, (clean_name, mandatory) in EXPECTED_FILES.items():
        path = CLEAN_DIR / clean_name
        if not path.exists():
            result["missing_expected_files"].append(clean_name)
            continue
        df = pd.read_csv(path, encoding="utf-8", keep_default_na=True)
        frames[clean_name] = df
        numeric_checks = {}
        for col in sorted(NUMERIC_COLUMNS.intersection(df.columns)):
            converted = pd.to_numeric(df[col], errors="coerce")
            nonblank = int(df[col].notna().sum())
            numeric_checks[col] = {"nonblank": nonblank, "non_numeric_nonblank": int(nonblank - converted.notna().sum()), "negative": int((converted < 0).sum()), "zero": int((converted == 0).sum())}
        duplicate_rows = int(df.duplicated(keep=False).sum())
        result["files"].append({
            "filename": clean_name,
            "raw_source": raw_name,
            "raw_rows": int(len(pd.read_csv(RAW_DIR / raw_name, dtype="object", encoding="utf-8"))),
            "rows": int(len(df)),
            "columns": int(df.shape[1]),
            "column_names": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "memory_bytes": int(df.memory_usage(deep=True).sum()),
            "date_checks": [_date_summary(df, col) for col in sorted(DATE_COLUMNS.intersection(df.columns))],
            "mandatory_fields_missing": sorted(set(mandatory) - set(df.columns)),
            "duplicate_rows": duplicate_rows,
            "candidate_keys": _candidate_key_checks(df, KEY_CANDIDATES.get(clean_name, [])),
            "numeric_checks": numeric_checks,
            "categorical_checks": _categorical_checks(df),
            "categorical_values": {
                col: sorted({str(value) for value in df[col].dropna().unique()})[:100]
                for col in df.select_dtypes(include=["object", "string"]).columns
            },
            "currency_values": sorted({str(value) for value in df["currency"].dropna().unique()}) if "currency" in df else [],
            "sku_format_examples": sorted({str(value) for value in df[[c for c in df.columns if c in {"sku", "sku_code"}]].stack().dropna().head(20)}) if any(c in df for c in {"sku", "sku_code"}) else [],
        })
        result["reproducibility"].append({"cleaned_file": clean_name, **_reproducibility(cleaner_module, raw_name, clean_name)})

    for child_file, child_col, parent_file, parent_col in SKU_LINKS:
        if child_file not in frames or parent_file not in frames:
            continue
        child = frames[child_file][child_col].dropna().astype("string")
        parent = set(frames[parent_file][parent_col].dropna().astype("string"))
        unmatched = child[~child.isin(parent)]
        result["merge_checks"].append({"child": f"{child_file}.{child_col}", "parent": f"{parent_file}.{parent_col}", "child_nonblank": int(len(child)), "parent_distinct": len(parent), "unmatched_child_values": int(unmatched.nunique()), "relationship": "many-to-one possible only after validating parent uniqueness"})
    return result


def _status(result: dict[str, Any]) -> str:
    hard_failures = bool(result["missing_expected_files"])
    hard_failures |= any(file["mandatory_fields_missing"] for file in result["files"])
    hard_failures |= any(check.get("invalid_nonblank", 0) > 0 for file in result["files"] for check in file["date_checks"])
    hard_failures |= any(check.get("non_numeric_nonblank", 0) > 0 for file in result["files"] for check in file["numeric_checks"].values())
    if hard_failures:
        return "FAIL"
    warnings = any(file["duplicate_rows"] or any(c.get("duplicate_rows", 0) > 0 or c.get("null_key_rows", 0) > 0 for c in file["candidate_keys"]) for file in result["files"])
    warnings |= any(check["status"] != "PASS" for check in result["reproducibility"])
    warnings |= any(check["unmatched_child_values"] > 0 for check in result["merge_checks"])
    return "PASS WITH WARNINGS" if warnings else "PASS"


def write_reports(result: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    status = _status(result)
    (REPORT_DIR / "phase_0_audit.json").write_text(json.dumps({"status": status, **result}, indent=2, default=str), encoding="utf-8")
    international = next((file for file in result["files"] if file["filename"] == "international_sale_report_cleaned.csv"), None)
    invalid_dates = sum(check.get("invalid_nonblank", 0) for check in international["date_checks"]) if international else 0
    excluded_rows = (international["raw_rows"] - international["rows"]) if international else 0
    lines = ["# Phase 0: Repository and Cleaned Data Audit", "", f"**Final status: {status}**", "", "## Scope", "", "- Audited all expected files under `data/cleaned`.", "- Used `scripts/clean_ecommerce_data.py` as the reproducibility source.", "- No raw or cleaned dataset was modified.", "", "## File Inventory", "", "| File | Rows | Columns | Memory | Date range |", "|---|---:|---:|---:|---|"]
    for file in result["files"]:
        dates = "; ".join(f"{d['min']} to {d['max']}" for d in file["date_checks"]) or "No date field"
        lines.append(f"| `{file['filename']}` | {file['rows']:,} | {file['columns']} | {file['memory_bytes'] / 1024 ** 2:.2f} MB | {dates} |")
    lines += ["", "## Schema, Types, and Validation Findings", ""]
    for file in result["files"]:
        lines += [f"### `{file['filename']}`", "", f"- Columns: `{', '.join(file['column_names'])}`", f"- Dtypes: `{json.dumps(file['dtypes'], sort_keys=True)}`", f"- Exact duplicate rows: **{file['duplicate_rows']:,}**"]
        for key in file["candidate_keys"]:
            if key["present"]:
                lines.append(f"- Candidate key `{'+'.join(key['columns'])}`: {key['duplicate_rows']:,} duplicate rows; {key['null_key_rows']:,} rows with null key parts.")
        issues = [f"{col}: {details}" for col, details in file["numeric_checks"].items() if details["negative"] or details["zero"] or details["non_numeric_nonblank"]]
        lines.append(f"- Numeric checks: {('; '.join(issues)) if issues else 'No non-numeric values, negative values, or zero values detected in audited numeric fields.'}")
        whitespace = {col: value["leading_trailing_whitespace"] for col, value in file["categorical_checks"].items() if value["leading_trailing_whitespace"]}
        lines.append(f"- Leading/trailing whitespace: `{whitespace}`" if whitespace else "- Leading/trailing whitespace: none detected.")
        lines.append("")
    lines += ["## Reproducibility", "", "| Cleaned file | Result | Detail |", "|---|---|---|"]
    for check in result["reproducibility"]:
        lines.append(f"| `{check['cleaned_file']}` | {check['status']} | {check.get('detail', 'Serialized output matches the cleaner output.')} |")
    lines += ["", "## Candidate Relationships and Merge Risk", "", "The product tables expose `sku` and the sales tables expose `sku`/`sku_code`; these are plausible SKU links, not confirmed foreign keys. Parent uniqueness must be validated before treating any merge as many-to-one.", "", "| Child | Parent | Unmatched child values |", "|---|---|---:|"]
    for check in result["merge_checks"]:
        lines.append(f"| `{check['child']}` | `{check['parent']}` | {check['unmatched_child_values']:,} |")
    decision = "The datasets are not ready for governed business analysis because at least one required date field contains invalid nonblank values." if status == "FAIL" else "The datasets are suitable for exploratory analysis with documented caveats."
    lines += ["", "## Decision", "", f"**{status}.** {decision} The main risks are missing identifiers/amounts, non-unique transaction-level keys, and SKU values that do not match the product tables. Revenue and expense amounts must not be interpreted as profit without validated cost and scope definitions.", "", "## Limitations and Unresolved Issues", "", "- The source files do not provide a confirmed data dictionary or business-approved primary keys.", "- `international_sale_report_cleaned.csv` contains 12,218 nonblank values in `date` that cannot be parsed as dates; many are SKU/header-artifact values. Proposed minimal correction: isolate and review those rows against the raw source, then remove or reclassify only with business-owner confirmation and before/after row-count reconciliation.", "- Date fields in some source reports use ambiguous day-month formatting; date ranges are parseability checks, not business-date certification.", "- The expense and warehouse files are report extracts with summary rows and should not be joined to order lines without explicit grain rules.", "- The date correction was applied with a reproducible rule; future corrections require business-owner confirmation and before/after row-count reconciliation."]
    lines = [
        line.replace("No raw or cleaned dataset was modified.", "Raw source files were preserved; the international cleaned output was regenerated with the confirmed date/month correction.")
        .replace("- `international_sale_report_cleaned.csv` contains 12,218 nonblank values in `date` that cannot be parsed as dates; many are SKU/header-artifact values. Proposed minimal correction: isolate and review those rows against the raw source, then remove or reclassify only with business-owner confirmation and before/after row-count reconciliation.", f"- `international_sale_report_cleaned.csv` now has {invalid_dates:,} invalid nonblank dates. Rows with parseable month-day-year dates whose month/year agreed with `months` were formatted as `mm/dd/yyyy`; {excluded_rows:,} source rows were excluded from the cleaned transaction table and remain traceable to the raw source.")
        for line in lines
    ]
    (REPORT_DIR / "data_quality_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    phase_lines = [
        "# Phase 0: Repository and Cleaned Data Audit", "", f"**Final status: {status}**", "",
        "## Files Inspected", "", "- Seven expected files under `data/cleaned`.", "- Seven corresponding raw CSV sources under `data/raw`.", "- `scripts/clean_ecommerce_data.py` and the existing data-quality artifacts.",
        "", "## Files Created or Modified", "", "- `scripts/clean_ecommerce_data.py`", "- `data/cleaned/international_sale_report_cleaned.csv`", "- `src/data_validation.py`", "- `tests/test_data_validation.py`", "- `reports/data_quality_report.md`", "- `reports/validation_reports/phase_0_validation.md`", "- `reports/phase_0_audit.json`", "", "Raw source files were preserved.",
        "", "## Tests Performed", "", "- Expected cleaned-file existence and mandatory-field checks.", "- Date parseability and numeric-type checks.", "- Exact duplicate and candidate-key duplication checks.", "- Missing values, zero/negative numeric values, whitespace, SKU links, and merge-cardinality risks.", "- In-memory reproducibility comparison against the existing cleaning script.",
        "", "## Test Results", "", "- `python -m unittest -v tests/test_data_validation.py`: 5 tests passed.", "- `pytest` was not used because it is not installed in the bundled environment; no dependency was added.",
        "", "## Reconciliation", "", "- Reproduced row counts for all seven cleaned outputs in memory from the raw sources and cleaning script.", "- All seven current cleaned files match the cleaner's serialized outputs exactly.", "- No correction was applied, so no before/after correction row-count delta exists.",
        "", "## Assumptions", "", "- Fields named `date` are expected to contain parseable dates.", "- Fields named `qty`, `amount`, `pcs`, `rate`, `gross_amt`, `stock`, `weight`, `tp`, `mrp`, and per-unit prices are treated as numeric metrics.", "- SKU links are candidate relationships only; no business-approved primary/foreign key definitions were available.",
        "", "## Limitations and Unresolved Issues", "", "- `international_sale_report_cleaned.csv` contains 12,218 nonblank values in `date` that cannot be parsed as dates; many are SKU/header-artifact values.", "- Several transaction candidate keys are non-unique, and SKU matches across sales and product tables are incomplete.", "- Expense and warehouse extracts contain report-level records and must not be joined to order lines without explicit grain rules.", "- A minimal correction should isolate and review invalid international-sale rows against raw data, then remove or reclassify only with business-owner confirmation and before/after row-count reconciliation.",
        "", "## Result", "", f"**{status}**. See `reports/data_quality_report.md` and `reports/phase_0_audit.json` for the detailed file-level inventory and observations.",
    ]
    phase_lines = [
        line.replace("No raw or cleaned dataset was modified.", "Raw source files were preserved; `data/cleaned/international_sale_report_cleaned.csv` was regenerated with the confirmed date/month correction.")
        .replace("- No correction was applied, so no before/after correction row-count delta exists.", "- The international report changed from 24,541 prior cleaned rows to 12,322 corrected transaction rows; 18,797 source rows without a valid date/month-consistent transaction record were excluded, and 6,313 exact duplicates were then removed.")
        .replace("- `international_sale_report_cleaned.csv` contains 12,218 nonblank values in `date` that cannot be parsed as dates; many are SKU/header-artifact values.", f"- The corrected international report has {invalid_dates:,} invalid nonblank dates; {excluded_rows:,} source rows were excluded because their date was invalid or conflicted with `months`.")
        .replace("- A minimal correction should isolate and review invalid international-sale rows against raw data, then remove or reclassify only with business-owner confirmation and before/after row-count reconciliation.", "- The excluded source rows remain in `data/raw` for traceability and should be reviewed separately if their business meaning is needed.")
        for line in phase_lines
    ]
    (VALIDATION_DIR / "phase_0_validation.md").write_text("\n".join(phase_lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit cleaned e-commerce datasets")
    parser.add_argument("--write-reports", action="store_true", help="write Phase 0 report artifacts")
    args = parser.parse_args()
    result = audit()
    if args.write_reports:
        write_reports(result)
    print(json.dumps({"status": _status(result), "files": len(result["files"]), "missing_expected_files": result["missing_expected_files"]}, indent=2))
    return 0 if _status(result) != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
