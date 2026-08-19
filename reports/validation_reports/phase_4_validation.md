# Phase 4 Validation: Sales Analytics

## Final status

**PASS WITH WARNINGS**

Phase 4 is limited to supported Amazon source-local reported measures,
international source-local gross measures, and explicitly labelled status
proxies. No net sales, profit, margin, customer, inventory, or causal KPI was
created.

## Files inspected and changed

Inspected:

- `PROJECT_RULES.md`
- `docs/kpi_definition.md`
- `docs/business_scope.md`
- `reports/validation_reports/remediation_01.md`
- `reports/validation_reports/remediation_02.md`
- `notebooks/03_sales_analytics.ipynb`
- Phase 3 SQL views and cleaned sales files

Changed:

- `notebooks/03_sales_analytics.ipynb`
- `reports/sales_findings.md`
- `reports/validation_reports/phase_4_validation.md`
- `tests/test_phase_4_revalidation.py`

No raw or cleaned source file was modified. Phase 0–3 analytical code was not
rebuilt.

## Supported metrics used

- Amazon reported gross amount, with amount coverage.
- Amazon distinct orders using distinct `order_id`.
- Amazon gross units.
- Daily, weekly, and monthly source-local reported trends.
- Complete-period month-over-month reported amount comparison.
- Source-local category, SKU, B2B, geography, and fulfilment mix.
- Amount concentration/Pareto within declared scopes.
- International reported gross amount and pieces, kept separate.

## Proxy metrics used

- `delivered_status_proxy` using exact status `Shipped - Delivered to Buyer`.
- Cancellation and return status composition using distinct Amazon orders.
- Reported amount per unit and reported amount per distinct order.

All proxy measures are labelled as analytical conventions, not official
completed-sales, cancellation, return, fulfilment, or revenue KPIs.

## Validation and reconciliation

| Result | SQL | Independent Pandas | Status |
|---|---:|---:|---|
| Amazon reported gross amount | 78,590,043.30 | 78,590,043.30 | PASS |
| Amazon distinct orders | 120,378 | 120,378 | PASS |
| Amazon gross units | 116,646 | 116,646 | PASS |
| Delivered-status-proxy amount | 18,650,815.00 | 18,650,815.00 | PASS |
| Delivered-status-proxy distinct orders | 26,566 | 26,566 | PASS |
| Delivered-status-proxy units | 28,886 | 28,886 | PASS |
| International reported gross amount | 10,834,927.19 | 10,834,927.19 | PASS |

Additional checks:

- Amount coverage is 93.96% overall, with 7,792 missing Amazon amounts; the
  notebook shows coverage beside monetary aggregations.
- Complete-month comparison reports April-to-May change of `-9.06%`; March and
  June boundary periods are suppressed from comparable MoM growth.
- Category and SKU concentration shares sum to 100% within their declared
  delivered-status-proxy scopes.
- Top-five category and SKU results are independently reproduced by direct
  Pandas group-bys.
- Order counts use `nunique(order_id)` and are not line counts.
- Amazon and international monetary values are never combined.
- The notebook executed top-to-bottom from a clean `python3` kernel with
  `ipykernel` already installed.
- Relevant Phase 4 tests and the full automated test suite passed.

## Excluded metrics

- Validated net sales, refund-adjusted sales, profit, margin, and customer KPIs.
- Official cancellation, return, fulfilment, delivery, and SLA rates.
- Inventory, stockout, and turnover KPIs.
- Seasonality, forecasting, causal, and elasticity claims.
- Cross-currency totals combining Amazon and international values.

## Remaining limitations

- `amount` is a reported field, not validated revenue or net sales; its missing
  business meaning remains unresolved.
- Status fields are source outcomes without event timestamps or approved order
  precedence.
- Amazon has only 91 observed dates and partial boundary months.
- International sales have no order ID, currency, or comparable B2B/platform
  fields.
- Cross-source SKU/category mappings remain unavailable.

## Decision

**PASS WITH WARNINGS.** Phase 4 is suitable for controlled descriptive sales
analysis under the approved governance. Stop here and wait before starting
Phase 5.
