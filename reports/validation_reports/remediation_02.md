# Remediation 2: EDA and SQL Revalidation

## Scope

Phase 2 EDA and Phase 3 SQL were revalidated against the Remediation 1 KPI
governance. Phase 0–1 were not re-audited; only direct documentation and
governance dependencies were used. Phases 4–9 were not started or recalculated.

## Files changed

- `notebooks/02_eda.ipynb`
- `sql/02_sales_analysis.sql`
- `sql/04_operations_analysis.sql`
- `docs/sql_analysis_notes.md`
- `data/processed/ecommerce.duckdb`
- `tests/test_remediation_02.py`
- `reports/validation_reports/remediation_02.md`

The SQL changes expose amount coverage and zero-value counts and label channel,
fulfilment, and stock outputs as source-local descriptive measures. No cleaned
source file was modified. `sql/01_data_validation.sql`,
`sql/03_product_analysis.sql`, and `scripts/run_sql_layer.py` were reviewed and
required no changes.

## EDA corrections

- The notebook now reports 91 observed Amazon dates explicitly.
- Amazon March and June and the international boundary months are labelled as
  partial periods.
- Missing Amazon `amount` coverage is printed and retained; no imputation or
  automatic deletion was added.
- Status outputs are labelled as analytical status proxies and not official
  cancellation, return, delivery, or completed-sales KPIs.
- Amazon and international monetary outputs remain in separate charts and
  tables.
- Existing text already excluded seasonality, causality, forecasting,
  profitability, and customer claims; those boundaries were preserved.

## SQL corrections

- Monthly Amazon views now expose `amount_lines`, `line_count`,
  `amount_coverage_pct`, `zero_amount_lines`, and `zero_quantity_lines`.
- NULL amounts remain excluded from `SUM(amount)` by SQL's native aggregate
  behavior and are now measurable through the coverage fields.
- Zero quantity and zero amount are reported, not silently removed.
- Channel and fulfilment outputs are labelled `source_local_*_mix` and remain
  source-local descriptive summaries.
- Stock outputs are labelled `stock_snapshot`; no dated inventory or turnover
  metric was added.
- No warehouse or expense table is joined to sales lines.
- No net sales, profit, margin, customer, or inventory-turnover view exists.
- Distinct order counts remain `COUNT(DISTINCT order_id)` and all ratios use
  `NULLIF` denominators.

## Validation and reconciliation

| Result | DuckDB | Independent Pandas | Status |
|---|---:|---:|---|
| Amazon row count | 128,969 | 128,969 | PASS |
| Amazon distinct orders | 120,378 | 120,378 | PASS |
| Amazon reported amount | 78,590,043.30 | 78,590,043.30 | PASS |
| Amazon reported units | 116,646 | 116,646 | PASS |
| International reported gross amount | 10,834,927.19 | 10,834,927.19 | PASS |
| Stock snapshot reported units | 242,386 | 242,386 | PASS |

Additional checks passed:

- Candidate Amazon-to-May product join did not multiply rows.
- Monthly amount coverage and zero-value counts reconcile to Pandas.
- NULL and zero denominator protections remain active.
- All four SQL files execute successfully in DuckDB.
- The EDA notebook executed top-to-bottom from a clean `python3` kernel after
  the sandbox kernel-port restriction was granted; `ipykernel` was already
  installed and no dependency was added.
- Phase 3 SQL tests and Remediation 2 tests passed.

## Remaining limitations

- Amazon amount is missing for 7,792 rows and its business meaning is unknown.
- Amazon and international monetary values cannot be combined because
  international currency is absent.
- Status metrics remain analytical proxies without an approved lifecycle rule.
- Amazon covers only 91 observed dates and has partial boundary months; no
  seasonality or forecasting claim is valid.
- Cross-source SKU matches remain unavailable, and stock is an undated,
  non-unique variant snapshot.
- Warehouse and expense data remain report/reference grains without sales keys.

## Phase status

- **Phase 2 EDA: PASS WITH WARNINGS.** Suitable for controlled descriptive EDA
  with source, date, amount, and proxy disclosures.
- **Phase 3 SQL: PASS WITH WARNINGS.** Reconciled and scoped to supported
  source-local metrics and explicitly labelled proxies.

## Stop decision

Remediation 2 is complete. Stop before Phase 4 and wait for approval.
