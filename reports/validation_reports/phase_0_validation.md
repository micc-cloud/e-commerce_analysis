# Phase 0: Repository and Cleaned Data Audit

**Final status: PASS WITH WARNINGS**

## Files Inspected

- Seven expected files under `data/cleaned`.
- Seven corresponding raw CSV sources under `data/raw`.
- `scripts/clean_ecommerce_data.py` and the existing data-quality artifacts.

## Files Created or Modified

- `scripts/clean_ecommerce_data.py`
- `data/cleaned/international_sale_report_cleaned.csv`
- `src/data_validation.py`
- `tests/test_data_validation.py`
- `reports/data_quality_report.md`
- `reports/validation_reports/phase_0_validation.md`
- `reports/phase_0_audit.json`

Raw source files were preserved.

## Tests Performed

- Expected cleaned-file existence and mandatory-field checks.
- Date parseability and numeric-type checks.
- Exact duplicate and candidate-key duplication checks.
- Missing values, zero/negative numeric values, whitespace, SKU links, and merge-cardinality risks.
- In-memory reproducibility comparison against the existing cleaning script.

## Test Results

- `python -m unittest -v tests/test_data_validation.py`: 5 tests passed.
- `pytest` was not used because it is not installed in the bundled environment; no dependency was added.

## Reconciliation

- Reproduced row counts for all seven cleaned outputs in memory from the raw sources and cleaning script.
- All seven current cleaned files match the cleaner's serialized outputs exactly.
- The international report changed from 24,541 prior cleaned rows to 12,322 corrected transaction rows; 18,797 source rows without a valid date/month-consistent transaction record were excluded, and 6,313 exact duplicates were then removed.

## Assumptions

- Fields named `date` are expected to contain parseable dates.
- Fields named `qty`, `amount`, `pcs`, `rate`, `gross_amt`, `stock`, `weight`, `tp`, `mrp`, and per-unit prices are treated as numeric metrics.
- SKU links are candidate relationships only; no business-approved primary/foreign key definitions were available.

## Limitations and Unresolved Issues

- The corrected international report has 0 invalid nonblank dates; 25,110 source rows were excluded because their date was invalid or conflicted with `months`.
- Several transaction candidate keys are non-unique, and SKU matches across sales and product tables are incomplete.
- Expense and warehouse extracts contain report-level records and must not be joined to order lines without explicit grain rules.
- The excluded source rows remain in `data/raw` for traceability and should be reviewed separately if their business meaning is needed.

## Result

**PASS WITH WARNINGS**. See `reports/data_quality_report.md` and `reports/phase_0_audit.json` for the detailed file-level inventory and observations.
