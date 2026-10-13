# Phase 9 Validation: Predictive Analytics Feasibility

## Final status

**PASS WITH WARNINGS**

The five proposed predictive use cases were assessed against the actual
cleaned datasets and completed analytical definitions. None passed the target,
predictor timing, validation, and actionability gates. The phase correctly
stopped without fitting a model.

## Rules and prior documentation reviewed

- `PROJECT_RULES.md`
- `docs/kpi_definition.md`
- `docs/data_dictionary.md`
- `docs/business_scope.md`
- `reports/eda_findings.md`
- `reports/sales_findings.md`
- `reports/product_findings.md`
- `reports/pricing_findings.md`
- `reports/operations_findings.md`
- `reports/profitability_feasibility.md`
- Phase 0 through Phase 8 validation reports

## Files inspected

- `data/cleaned/amazon_sale_report_cleaned.csv`
- `data/cleaned/international_sale_report_cleaned.csv`
- `data/cleaned/may_2022_cleaned.csv`
- `data/cleaned/p_l_march_2021_cleaned.csv`
- `data/cleaned/sale_report_cleaned.csv`
- `data/cleaned/cloud_warehouse_compersion_chart_cleaned.csv`
- `data/cleaned/expense_iigf_cleaned.csv`

## Files created

- `reports/predictive_feasibility.md`
- `reports/validation_reports/phase_9_validation.md`
- `tests/test_phase_9_predictive.py`

`notebooks/08_predictive_analysis.ipynb` was intentionally not created because
no use case was sufficiently valid.

## Validation performed

- Confirmed actual date ranges and date counts for Amazon and international
  sales.
- Confirmed Amazon order and status-proxy counts using distinct `order_id`.
- Examined status-proxy class balance for cancellation and return candidates.
- Checked available fields for target leakage, event timing, customer history,
  inventory history, and cost support.
- Confirmed that no target can be defined as a validated profit or margin
  measure.
- Confirmed that no train/test split, model comparison, or notebook rerun was
  performed because the feasibility gate failed.

## Required modelling controls if feasibility is later approved

- Define the target and the exact prediction-time cutoff.
- Exclude status, courier, refund, and other post-cutoff fields.
- Fit all preprocessing on training data only.
- Use a chronological or rolling-origin split; do not use a random split for
  temporal prediction.
- Compare against a naive baseline before considering up to three simple
  models.
- Report business-relevant errors, class imbalance, calibration, and error
  segments.
- Re-run the notebook from a clean kernel and record the result.

## Reconciliation, assumptions, and limitations

No predictive output was produced, so there is no model reconciliation or
performance claim. Dataset counts and date ranges were checked against the
cleaned CSV files. The assessment assumes that status and courier fields are
not guaranteed to be available before the business action; this is an explicit
data-lineage gap requiring source-system confirmation, not a fabricated
business rule.

The principal unresolved issues are short history, partial periods, missing
event timestamps, status-proxy targets, sparse SKU-date observations, absent
inventory history, absent customer IDs, and absent costed profit data.

## Scope decision

Stop Phase 9 after feasibility assessment. Reopen only after the minimum data
and business decision requirements in `reports/predictive_feasibility.md` are
approved.
