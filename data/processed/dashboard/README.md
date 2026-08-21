# Power BI Dashboard Data Package

These CSVs are derived from `data/cleaned/` by
`scripts/build_dashboard_package.py`. They are intended for manual import into
Power BI Desktop. No `.pbix` file is included.

| File | Grain | Use |
|---|---|---|
| `fact_amazon_sales.csv` | One Amazon source order-line record | Main Amazon sales, product, pricing-proxy, and source-status visuals |
| `dim_date.csv` | One observed Amazon date | Date filtering and partial-period warnings |
| `dim_category.csv` | One Amazon source-local category | Category filtering |
| `dim_sku.csv` | One Amazon source-local SKU | SKU filtering and drill-through |
| `dim_order_status.csv` | One distinct Amazon order | Order-level status composition and mixed-status governance |
| `fact_international_sales.csv` | One retained international sales line | Separate international pieces and gross amount; no relationship to Amazon |

Load all six CSVs. Create relationships exactly as documented in
`docs/power_bi_model.md`; do not create cross-source SKU, currency, product,
stock, warehouse, or expense relationships.

Important labels:

- Amazon `amount` is **Reported Gross Amount**, not net sales.
- `amount / qty` is **Reported Unit-Price Proxy**, not realised selling price.
- Status measures are **Status Composition Proxies**, not official rates.
- International monetary values have unspecified currency and must remain
  separate from Amazon INR values.
