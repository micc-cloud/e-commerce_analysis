# Phase 10 Validation: Power BI Build Package

## Final status

**PASS WITH WARNINGS**

The repository now contains a manually loadable Power BI build package and
documentation. No `.pbix` file was created, edited, or simulated. The package
supports source-local Amazon descriptive reporting and a separate international
fact table.

## Files created or changed

Created:

- `data/processed/dashboard/README.md`
- `data/processed/dashboard/fact_amazon_sales.csv`
- `data/processed/dashboard/dim_date.csv`
- `data/processed/dashboard/dim_category.csv`
- `data/processed/dashboard/dim_sku.csv`
- `data/processed/dashboard/dim_order_status.csv`
- `data/processed/dashboard/fact_international_sales.csv`
- `scripts/build_dashboard_package.py`
- `docs/power_bi_model.md`
- `docs/dax_measures.md`
- `docs/dashboard_specification.md`
- `docs/power_bi_build_guide.md`
- `tests/test_phase_10_power_bi.py`
- `reports/validation_reports/phase_10_validation.md`

Documentation consistency repair:

- `reports/validation_reports/phase_8_validation.md` now lists the actual
  cleaned filenames required by the existing remediation test. Its feasibility
  decision and analytical content were not changed.

No cleaned or raw source file was modified. No `.pbix` file exists in the
package.

## Dashboard tables prepared

| Table | Rows | Grain | Key status |
|---|---:|---|---|
| `fact_amazon_sales` | 128,969 | Amazon source order-line record | `order_id` repeats; no line primary key |
| `dim_date` | 91 | Observed Amazon date | Unique `date_key` |
| `dim_category` | 9 | Amazon source-local category | Unique `category_key` |
| `dim_sku` | 7,195 | Amazon source-local SKU | Unique `sku_key` |
| `dim_order_status` | 120,378 | Distinct Amazon order | Unique `order_id` |
| `fact_international_sales` | 12,322 | International source sales line | No order key; standalone |

## Proposed relationships

| Relationship | Cardinality | Filter direction | Validation |
|---|---|---|---|
| `dim_date[date_key]` -> `fact_amazon_sales[date_key]` | 1 : * | Single | Dimension key unique and all fact dates covered |
| `dim_category[category_key]` -> `fact_amazon_sales[category]` | 1 : * | Single | Category key unique and all non-null fact categories covered |
| `dim_sku[sku_key]` -> `fact_amazon_sales[sku]` | 1 : * | Single | SKU key unique and all fact SKUs covered |
| `dim_order_status[order_id]` -> `fact_amazon_sales[order_id]` | 1 : * | Single | Order key unique and all fact orders covered |

No relationship is proposed for `fact_international_sales`. No Amazon-to-MRP,
stock, warehouse, expense, or international relationship is safe.

## DAX measures prepared

Supported measures:

- Reported Gross Amount
- Amount Coverage %
- Distinct Orders
- Gross Units
- B2B Orders, B2C Orders, and B2B Mix %
- Category Contribution %
- SKU Contribution %
- International Reported Gross Amount (Currency Unspecified)
- International Reported Pieces

Proxy measures:

- Reported Unit-Price Proxy, restricted to valid delivered-status-proxy rows
- Status Composition %
- Cancelled, Return-Related, and Delivered Status Proxy Orders

All formulas, definitions, classifications, and limitations are documented in
`docs/dax_measures.md`. No profit, margin, net sales, customer, inventory
turnover, forecast, predictive, official cancellation/return rate, SLA, or
delivery-time measure is defined.

## Reconciliation results

| Metric | Dashboard package | Validated source / Phase 4–7 | Status |
|---|---:|---:|---|
| Amazon rows | 128,969 | 128,969 | PASS |
| Amazon reported gross amount | 78,590,043.30 | 78,590,043.30 | PASS |
| Amazon distinct orders | 120,378 | 120,378 | PASS |
| Amazon gross units | 116,646 | 116,646 | PASS |
| Amazon amount coverage | 93.96% | 93.96% | PASS |
| Delivered status proxy rows | 28,769 | 28,769 | PASS |
| Valid delivered proxy price rows | 28,761 | 28,761 | PASS |
| Mixed-status orders | 0 | 0 | PASS WITH WARNING |
| International rows | 12,322 | 12,322 | PASS |

The dashboard builder was rerun from the cleaned files after a focused repair
to ensure `dim_date.csv` and the validated price-band field are generated. The
Amazon fact retains the 26 fields required by the four-page specification and
omits unused source columns to keep the Power BI import package lightweight.

## Tests performed

- `python -m unittest -q tests/test_phase_10_power_bi.py`: **6 passed**.
- Confirmed all six CSV tables load with Pandas.
- Confirmed all dimension keys are unique.
- Confirmed relationship key coverage and no many-to-many relationship is
  proposed.
- Confirmed the pricing proxy uses amount present, positive quantity, and the
  delivered-status proxy.
- Confirmed international monetary fields remain isolated and currency is not
  invented.
- Confirmed partial-period metadata marks March and June 2022.
- Confirmed documentation includes proxy labels, amount coverage disclosure,
  relationship direction, and blocked metrics.
- Confirmed no `.pbix` file was created.
- `git diff --check`: passed.

## Remaining limitations

- Power BI Desktop itself was not run in this environment; manual import and
  relationship creation remain to be completed by the user.
- Amount coverage is incomplete and reported amount is not net sales.
- The pricing proxy is not realised selling price and uses a status convention.
- Status measures are source-status composition proxies without precedence or
  event timestamps.
- International currency is unspecified and no cross-source monetary total is
  valid.
- The package intentionally excludes blocked profitability and predictive
  analytics.

## Decision

**PASS WITH WARNINGS.** The files are ready for manual Power BI Desktop build
within the documented four-page scope. Keep all warnings and proxy labels
visible in the report.
