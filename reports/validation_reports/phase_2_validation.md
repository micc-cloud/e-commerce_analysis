# Phase 2: Exploratory Data Analysis Validation

**Final status: PASS WITH WARNINGS**

## Files inspected

- `data/cleaned/*.csv` (seven cleaned datasets).
- `reports/data_quality_report.md`.
- `reports/validation_reports/phase_0_validation.md`.
- `reports/validation_reports/phase_1_validation.md`.
- `docs/kpi_definition.md` and `docs/business_scope.md`.
- Existing `scripts/EDA.py` and the prior business-focused notebook.

## Files created or modified

- `notebooks/02_eda.ipynb`
- `scripts/EDA.py` (replaced the over-generalized Plotly/Seaborn workflow)
- `scripts/build_eda_notebook.py`
- `src/visualizations.py`
- `reports/eda_findings.md`
- `reports/validation_reports/phase_2_validation.md`
- `reports/eda_outputs/dataset_quality_summary.csv`
- `reports/eda_outputs/amazon_monthly_summary.csv`
- `reports/eda_outputs/international_monthly_summary.csv`

No later-phase notebook or profitability model was created.

## Notebook structure validated

The notebook contains the required sections: objective, loading, validation, grain/coverage, numerical distributions, categorical distributions, date trends, status analysis, SKU/category coverage, supported channel/fulfilment analysis, outlier investigation, preliminary relationships, findings, follow-up questions, and limitations.

Each chart section states a business question, observation, interpretation, and limitation. Outliers are flagged for investigation and retained.

## Tests performed and results

- Loaded all seven cleaned datasets and asserted expected fields.
- Confirmed corrected date parsing for Amazon `%Y-%m-%d` and international `%m/%d/%Y`.
- Confirmed international date months match the `months` field.
- Confirmed no exact duplicate rows in the seven cleaned datasets.
- Confirmed numerical fields used in EDA are numerical.
- Reconciled three important aggregations independently:
  - Amazon reported amount equals the sum of monthly group-by amounts: `78,590,043.30`.
  - Amazon distinct orders equal the sum of monthly distinct-order counts: `120,378`.
  - International gross amount equals the sum of monthly group-by gross amounts: `10,834,927.19`.
- Confirmed monthly tables keep `line_count` separate from `distinct_orders`.
- Confirmed cancelled and returned labels are shown as status proxies and are not silently netted.
- Confirmed source tables have no exact duplicates; missing SKU/category fields remain disclosed.
- `scripts/EDA.py` executed successfully and wrote summary tables.
- All 14 notebook code cells executed sequentially in a fresh Python process with `MPLBACKEND=Agg`.
- A true Jupyter kernel restart/`nbconvert --execute` could not be run because no `python3` kernelspec or `ipykernel` is installed in the environment. This is an environment limitation, not a notebook-cell failure.

## Grain and denominator controls

- Amazon order counts use `nunique(order_id)`, never row count.
- Amazon sales and units remain at line grain; monthly tables show line count and distinct orders separately.
- International sales remain a separate line-grain source with no order identifier or currency.
- Stock is treated as a snapshot table; no turnover or time-based stockout KPI is calculated.
- No customer-level KPI is calculated from the non-ID `customer` text field.

## Findings and limitations

- Amazon has 128,969 order lines and 120,378 distinct orders in the observed window.
- International sales have 12,322 retained lines; their reported gross amount is kept separate because currency is absent.
- Amazon includes cancellation and return-related statuses, but status proxies are not presented as true rates.
- Cross-source SKU matches are incomplete, so product enrichment is not assumed to be complete.
- Extreme values are retained and presented as investigation candidates.
- Profit, margin, true net sales, customer-360, true return rate, delivery-time, and inventory-turnover analysis remain excluded under Phase 1 rules.

## Validation decision

**PASS WITH WARNINGS.** The EDA is reproducible and suitable for descriptive analysis. Before downstream KPI or modelling work, the project should establish business-approved status precedence, SKU mapping, currency coverage, and cost/inventory definitions.
