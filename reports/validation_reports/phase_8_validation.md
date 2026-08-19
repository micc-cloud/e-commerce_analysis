# Phase 8 Validation: Profitability Feasibility

## Final status

**PASS WITH WARNINGS**

The feasibility assessment completed successfully and correctly stopped before
profitability analysis. The available data is insufficient for defensible
profitability metrics.

## Rules and definitions reviewed

- `PROJECT_RULES.md`
- `docs/kpi_definition.md`
- `docs/data_dictionary.md`
- Phase 0 through Phase 7 validation reports

The approved definitions explicitly state that profit, gross margin, and true
net sales are unsupported without reliable cost, matching, currency, and
transaction treatment.

## Files inspected

- `data/cleaned/amazon_sale_report_cleaned.csv`
- `data/cleaned/international_sale_report_cleaned.csv`
- `data/cleaned/may_2022_cleaned.csv`
- `data/cleaned/p_l_march_2021_cleaned.csv`
- `data/cleaned/cloud_warehouse_compersion_chart_cleaned.csv`
- `data/cleaned/expense_iigf_cleaned.csv`
- `data/cleaned/sale_report_cleaned.csv`

## Files created

- `reports/profitability_feasibility.md`
- `reports/validation_reports/phase_8_validation.md`
- `tests/test_phase_8_profitability.py`

`notebooks/07_profitability_analytics.ipynb` and
`reports/profitability_findings.md` were intentionally not created because the
feasibility gate failed.

## Validation performed

- Confirmed that no COGS/product-cost field is defined or transaction-linked.
- Confirmed that no platform-fee, shipping-cost, tax, refund-value, or return-
  quantity field is available.
- Confirmed that Amazon has order IDs and dates but the warehouse and expense
  sources lack reliable sales keys and dates.
- Confirmed that Amazon amount coverage is incomplete and that its amount field
  is not approved as realised net revenue.
- Confirmed that product snapshot SKU matching cannot provide a reliable cost
  join.
- Confirmed that warehouse rates cannot be allocated to transactions.
- Confirmed that expense detail and summary/balance rows must not be combined.
- Confirmed that no profitability reconciliation or margin calculation was
  performed, because doing so would require unsupported assumptions.

## Reconciliation and limitations

Sales-level reported amounts remain subject to the limitations documented in
Phases 0, 1, and 4. A sales total can be reconciled to the sales analysis, but
there is no valid net-revenue or cost total against which to reconcile profit.
Returns, cancellations, fees, taxes, currency conversion, and expense
allocation therefore remain unresolved.

## Scope decision

The phase stops after feasibility assessment as required. Profitability
analysis may resume only after the additional data and definitions listed in
`reports/profitability_feasibility.md` are approved.
