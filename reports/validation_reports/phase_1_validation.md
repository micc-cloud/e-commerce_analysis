# Phase 1: Business Scope and KPI Feasibility Validation

**Final status: PASS WITH WARNINGS**

## Files inspected

- Seven cleaned datasets under `data/cleaned`.
- `reports/data_quality_report.md`.
- `reports/validation_reports/phase_0_validation.md`.
- `scripts/clean_ecommerce_data.py` and `src/data_validation.py`.

## Files created

- `docs/data_dictionary.md`
- `docs/kpi_definition.md`
- `docs/business_scope.md`
- `images/data_model.svg`
- `tests/test_phase_1_scope.py`
- `reports/validation_reports/phase_1_validation.md`

No EDA notebook was created or modified.

## Tests performed and results

- Confirmed every required field referenced by the KPI matrix exists in the relevant cleaned file.
- Confirmed each documented table grain is supported by observed key behavior: Amazon `order_id` repeats, product `sku` is unique in the product snapshots, and `sku_code` is not unique in the stock report.
- Confirmed date, quantity, amount, rate, gross amount, and stock fields referenced by formulas exist with numerical/date-compatible representations.
- Confirmed formulas use source column names and define order-level denominators with `COUNT(DISTINCT order_id)`.
- Confirmed cancelled/returned statuses are treated as explicit status scopes or limitations rather than silently netted.
- Confirmed no reliable customer ID is invented; customer-level KPIs are excluded.
- Confirmed the SVG data-model diagram exists and distinguishes candidate links from confirmed relationships.
- `python -m unittest -v tests/test_phase_1_scope.py`: 3 tests passed.

## Reconciliation and grain controls

- Amazon sales calculations must remain at line grain for `SUM(qty)`/`SUM(amount)` and use distinct `order_id` only for order denominators.
- International sales calculations must remain separate because the table has no order ID and no currency field.
- Product snapshots contain 1,330 unique `sku` values each, but sales-to-product match rates are incomplete.
- The stock report has 9,233 rows and non-unique `sku_code`; it cannot be treated as a one-row-per-SKU master without further deduplication rules.
- Warehouse and expense reports have no confirmed sales key and cannot be allocated to orders or lines.

## Assumptions

- `amount` and `gross_amt` are reported monetary fields, not proven net sales or profit.
- `status` labels are usable for descriptive status analysis, but an order-level precedence rule is required when lines within an order differ.
- `tp`, `tp_1`, and `tp_2` are reference price fields until their business definitions are confirmed.
- The realistic scenario is an apparel e-commerce business with Amazon, international sales, product-price snapshots, and a stock snapshot.

## Limitations and unresolved issues

- International sales have no order identifier, customer identifier, or currency field.
- Amazon amount and currency are missing on a subset of rows; cancellation/return/refund values are not separately provided.
- SKU match gaps prevent unqualified cross-source product or price analysis.
- Profit, gross margin, true net sales, true return rate, customer-360 metrics, inventory turnover, and delivery-time KPIs are unsupported and explicitly excluded.
- The source does not define the period, unit, or accounting basis for warehouse rates and expense amounts.

## Validation decision

**PASS WITH WARNINGS.** The business scope and KPI definitions are feasible for a controlled sales, product, pricing-reference, and operational-status analysis. Downstream analysis must use the documented source-specific scopes and must not present unsupported profitability, customer, return, or inventory-turnover conclusions.
