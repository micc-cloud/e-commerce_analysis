# Phase 4 Validation: Sales Analytics

## Decision

**PASS WITH WARNINGS**

The sales analytics notebook ran from top to bottom in a fresh Python process. Supported gross-value, order, unit, time-trend, contribution, and descriptive segment measures were reconciled. Net sales and profitability remain explicitly out of scope.

## Environment and dependencies

- Python 3.10.14 analysis runtime
- pandas 2.3.3
- matplotlib 3.10.8
- DuckDB 1.5.5
- Existing DuckDB database: `data/processed/ecommerce.duckdb`
- No new project dependency was added to `requirements.txt`.

## Files inspected and changed

- Inspected: `PROJECT_RULES.md`, `docs/kpi_definition.md`, `reports/validation_reports/phase_3_validation.md`, cleaned CSVs, and Phase 3 SQL outputs.
- Created: `notebooks/03_sales_analytics.ipynb`, `reports/sales_findings.md`, `reports/validation_reports/phase_4_validation.md`, and `tests/test_phase_4_sales.py`.
- The cleaned datasets were not modified.

## Validation performed

- The notebook was executed sequentially in a fresh Python process; all 32 cells completed without errors.
- Amazon reported amount reconciled to DuckDB: `78,590,043.30`.
- Amazon distinct orders reconciled to DuckDB: `120,378`.
- Amazon units reconciled to DuckDB: `116,646`.
- International gross amount reconciled to DuckDB: `10,834,927.19`.
- Order counts use distinct `order_id`; line counts are shown separately.
- MoM growth uses a guarded denominator and suppresses comparisons involving partial March and June boundary months. May versus April is `-9.06%`.
- Category and attributed-SKU concentration shares each sum to 100% within their own denominator.
- Top five category and SKU results were independently reproduced with direct pandas group-bys.
- No outliers were removed. Daily IQR screening flagged no days above the calculated upper bound.

## Assumptions and limitations

- “Reported gross sales” means the sum of the available `amount` field for Amazon; it is not asserted to be net sales or profit.
- Reported gross sales, units, and order counts use the available source rows. Cancelled and returned records were not silently reclassified or removed because no approved order-level status precedence rule exists; therefore these are not completed-order measures.
- Amazon and international values are kept separate because the international file has no currency field and no comparable order identifier.
- AOV is not claimed as a fully validated KPI; the notebook reports reported amount per distinct order as a clearly labelled proxy.
- Partial months are extract-boundary months, not necessarily calendar months with missing business activity.
- Shipping geography is descriptive and does not support customer-level analysis.
- The notebook was replayed programmatically rather than through a Jupyter kernel because the runtime has no registered Jupyter kernelspec; sequential execution still covered every cell.

## Final status

**PASS WITH WARNINGS**: suitable for supported sales analysis with the limitations above. Do not use the outputs for net sales, profitability, customer analytics, true return rate, or inventory turnover.
