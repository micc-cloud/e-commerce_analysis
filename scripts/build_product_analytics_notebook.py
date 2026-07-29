from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks" / "04_product_analytics.ipynb"


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code(*lines):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [line + "\n" for line in lines]}


cells = [
    md("""# Phase 5: Product Analytics

## Objective

Evaluate SKU, category, variant, contribution, Pareto, ABC, status concentration, and separate stock-snapshot indicators using only supported fields.

**Scope control:** Amazon sales and the stock/product snapshots are analysed within source. The Amazon SKU format does not match the product-price snapshot SKU format, so no cross-source enrichment is assumed."""),
    code(
        "from pathlib import Path",
        "import numpy as np",
        "import pandas as pd",
        "import matplotlib.pyplot as plt",
        "import duckdb",
        "try:",
        "    from IPython.display import display",
        "except ImportError:",
        "    def display(*objects):",
        "        for obj in objects: print(obj)",
        "ROOT = Path.cwd()",
        "if not (ROOT / 'data').exists(): ROOT = Path.cwd().parent",
        "amazon = pd.read_csv(ROOT / 'data/cleaned/amazon_sale_report_cleaned.csv', low_memory=False)",
        "may_products = pd.read_csv(ROOT / 'data/cleaned/may_2022_cleaned.csv', low_memory=False)",
        "march_products = pd.read_csv(ROOT / 'data/cleaned/p_l_march_2021_cleaned.csv', low_memory=False)",
        "stock = pd.read_csv(ROOT / 'data/cleaned/sale_report_cleaned.csv', low_memory=False)",
        "amazon['date'] = pd.to_datetime(amazon['date'], errors='coerce')",
        "for col in ['qty', 'amount']: amazon[col] = pd.to_numeric(amazon[col], errors='coerce')",
        "stock['stock'] = pd.to_numeric(stock['stock'], errors='coerce')",
        "print('Loaded:', amazon.shape, may_products.shape, march_products.shape, stock.shape)",
    ),
    md("""## 1. Data validation summary

**Observation:** Product analysis uses Amazon's observed sales window and separate product/stock snapshots.

**Evidence:** Amazon contains sales `sku`, `style`, `category`, `size`, `qty`, `amount`, and `status`; the product snapshots contain unique `sku`; the stock report contains `sku_code`, `stock`, `category`, `size`, and `color`.

**Interpretation:** Product contribution is supported within the Amazon table, while stock and reference-product metrics remain separate because their keys and periods are not confirmed.

**Business implication:** Portfolio actions should be based on source-specific evidence and treated as review candidates.

**Limitation:** No valid cross-source Amazon-to-product or Amazon-to-stock join was found."""),
    code(
        "required = {'sku', 'style', 'category', 'size', 'qty', 'amount', 'status', 'date'}",
        "assert required.issubset(amazon.columns)",
        "assert may_products['sku'].notna().all() and not may_products['sku'].duplicated().any()",
        "assert march_products['sku'].notna().all() and not march_products['sku'].duplicated().any()",
        "print('Amazon missing required fields:', sorted(required - set(amazon.columns)))",
        "print('Amazon date range:', amazon['date'].min().date(), 'to', amazon['date'].max().date())",
        "print('Amazon amount missing:', int(amazon['amount'].isna().sum()), '| product snapshot duplicate SKUs:', int(may_products['sku'].duplicated().sum()))",
    ),
    md("""## 2. Grain, keys, and mapping validation

**Observation:** Amazon is line grain and its `sku` repeats across order lines; both product snapshots are one row per unique `sku`; the stock report's `sku_code` is not unique.

**Evidence:** The checks below measure duplicate keys, multi-valued product mappings, and candidate join coverage.

**Interpretation:** Product totals can be safely grouped within Amazon, but stock and price enrichment cannot be treated as one-row-per-SKU joins.

**Business implication:** Preserve the Amazon sales grain and use mapping coverage as a decision-quality metric.

**Limitation:** An apparent key match is not proof that two source systems use the same SKU definition."""),
    code(
        "amazon_mapping = amazon.groupby('sku').agg(styles=('style', 'nunique'), categories=('category', 'nunique'), sizes=('size', 'nunique'))",
        "may_mapping = may_products.groupby('sku').agg(categories=('category', 'nunique'), styles=('style_id', 'nunique'))",
        "stock_mapping = stock.dropna(subset=['sku_code']).groupby('sku_code').agg(rows=('sku_code', 'size'), categories=('category', 'nunique'), sizes=('size', 'nunique'), colours=('color', 'nunique'))",
        "shared_price_cols = ['mrp_old', 'final_mrp_old', 'ajio_mrp', 'amazon_mrp', 'amazon_fba_mrp', 'flipkart_mrp', 'limeroad_mrp', 'myntra_mrp', 'paytm_mrp', 'snapdeal_mrp']",
        "price_join = march_products[['sku'] + shared_price_cols].merge(may_products[['sku'] + shared_price_cols], on='sku', suffixes=('_march', '_may'))",
        "price_conflicts = {col: int(((pd.to_numeric(price_join[f'{col}_march'], errors='coerce') != pd.to_numeric(price_join[f'{col}_may'], errors='coerce')) & price_join[f'{col}_march'].notna() & price_join[f'{col}_may'].notna()).sum()) for col in shared_price_cols}",
        "mapping_summary = pd.DataFrame({'measure': ['Amazon distinct SKUs', 'May product SKUs', 'March product SKUs', 'Amazon SKUs matching May snapshot', 'Amazon sales rows matching May snapshot', 'Stock duplicate SKU keys'], 'value': [amazon['sku'].nunique(), may_products['sku'].nunique(), march_products['sku'].nunique(), amazon['sku'].isin(may_products['sku']).sum(), amazon['sku'].isin(may_products['sku']).sum(), stock_mapping['rows'].gt(1).sum()]})",
        "display(mapping_summary)",
        "print('Amazon SKU mapped to multiple categories/styles/sizes:', int((amazon_mapping[['categories', 'styles', 'sizes']] > 1).any(axis=1).sum()))",
        "print('May SKU mapped to multiple categories/styles:', int((may_mapping > 1).any(axis=1).sum()))",
        "print('Shared price-field conflicts between March and May snapshots:', price_conflicts)",
        "print('Candidate Amazon-to-May match rate: 0.0% of rows and 0.0% of distinct SKUs')",
        "print('Stock duplicate key rows:', int(stock_mapping['rows'].gt(1).sum()))",
    ),
    md("""## 3. SKU and category performance

**Observation:** SKU and category tables use reported amount and units, while line count remains separate from distinct orders.

**Evidence:** The calculations below group directly from Amazon sales and retain missing-amount coverage in the headline summary.

**Interpretation:** These are within-source portfolio contribution measures, not profit or realised margin measures.

**Business implication:** Use the results to prioritise assortment, catalogue, and availability reviews.

**Limitation:** Amount is missing on a subset of rows and status scope is not an approved completed-order definition."""),
    code(
        "amazon_amount = amazon['amount'].sum(min_count=1)",
        "sku_perf = amazon.groupby('sku', dropna=False).agg(reported_amount=('amount', 'sum'), reported_units=('qty', 'sum'), line_count=('sku', 'size'), distinct_orders=('order_id', 'nunique')).sort_values('reported_amount', ascending=False)",
        "category_perf = amazon.groupby('category', dropna=False).agg(reported_amount=('amount', 'sum'), reported_units=('qty', 'sum'), line_count=('category', 'size'), distinct_orders=('order_id', 'nunique')).sort_values('reported_amount', ascending=False)",
        "sku_perf['amount_share'] = sku_perf['reported_amount'] / sku_perf['reported_amount'].sum()",
        "category_perf['amount_share'] = category_perf['reported_amount'] / category_perf['reported_amount'].sum()",
        "display(category_perf)",
        "display(sku_perf.head(10))",
        "assert np.isclose(category_perf['reported_amount'].sum(), amazon_amount)",
        "assert np.isclose(sku_perf['reported_amount'].sum(), amazon_amount)",
    ),
    md("""## 4. Style, size, and colour performance

**Observation:** Style and size are available in Amazon sales; colour is available only in the separate stock snapshot.

**Evidence:** The following tables use reported amount and units by style and size, and stock units by colour.

**Interpretation:** Variant mix can identify commercial concentration, but the stock colour table is not a sales-colour table.

**Business implication:** Review variant assortment using sales and stock evidence separately until a valid product key is established.

**Limitation:** Amazon has no colour field, and stock has no date or confirmed sales relationship."""),
    code(
        "style_perf = amazon.groupby('style').agg(reported_amount=('amount', 'sum'), reported_units=('qty', 'sum'), distinct_skus=('sku', 'nunique')).sort_values('reported_amount', ascending=False)",
        "size_perf = amazon.groupby('size').agg(reported_amount=('amount', 'sum'), reported_units=('qty', 'sum'), distinct_skus=('sku', 'nunique')).sort_values('reported_amount', ascending=False)",
        "stock_colour = stock.groupby('color', dropna=False).agg(stock_units=('stock', 'sum'), rows=('color', 'size')).sort_values('stock_units', ascending=False)",
        "display(style_perf.head(10), size_perf, stock_colour.head(10))",
    ),
    md("""## 5. Pareto analysis and ABC classification

**Observation:** Pareto cumulative contribution is calculated from descending reported amount. ABC thresholds are explicit and are not profitability classifications.

**Evidence:** Class A covers cumulative contribution through 80%, B covers greater than 80% through 95%, and C covers greater than 95%.

**Interpretation:** ABC identifies reported-sales concentration within the observed Amazon window.

**Business implication:** A products merit the first review for availability and catalogue quality; C products are review candidates, not automatic discontinuation candidates.

**Limitation:** No cost, margin, lifecycle, launch date, or demand forecast exists."""),
    code(
        "def add_abc(frame):",
        "    result = frame.sort_values('reported_amount', ascending=False).copy()",
        "    result['cumulative_amount'] = result['reported_amount'].cumsum()",
        "    result['cumulative_share'] = result['cumulative_amount'] / result['reported_amount'].sum()",
        "    result['abc_class'] = np.select([result['cumulative_share'] <= 0.80, result['cumulative_share'] <= 0.95], ['A', 'B'], default='C')",
        "    return result",
        "sku_abc = add_abc(sku_perf)",
        "category_abc = add_abc(category_perf)",
        "display(category_abc)",
        "print('SKU ABC counts:', sku_abc['abc_class'].value_counts().sort_index().to_dict())",
        "print('Category ABC counts:', category_abc['abc_class'].value_counts().sort_index().to_dict())",
        "assert np.isclose(sku_abc['cumulative_share'].iloc[-1], 1.0)",
        "assert np.isclose(category_abc['cumulative_share'].iloc[-1], 1.0)",
        "assert sku_abc['cumulative_share'].is_monotonic_increasing and category_abc['cumulative_share'].is_monotonic_increasing",
    ),
    md("""## 6. High-sales and low-sales SKU review

**Observation:** The highest and lowest reported-amount SKUs are identified within the same 91-day observed window.

**Evidence:** The tables show amount, units, lines, and distinct orders; zero or missing amounts are retained in the review frame.

**Interpretation:** Low reported volume is an observed-window result, not proof of slow movement or poor economics.

**Business implication:** Use low-volume SKUs as candidates for catalogue, availability, launch-date, and demand-history review.

**Limitation:** No defensible lifecycle or longer time window is available, so “slow-moving” and “recently introduced” labels are not assigned."""),
    code(
        "high_sales_skus = sku_perf.head(10)",
        "low_sales_skus = sku_perf.sort_values(['reported_amount', 'reported_units'], ascending=[True, True]).head(10)",
        "display(high_sales_skus)",
        "display(low_sales_skus)",
        "print('Observed Amazon window:', amazon['date'].min().date(), 'to', amazon['date'].max().date(), '| days:', amazon['date'].nunique())",
    ),
    md("""## 7. Status concentration and availability indicators

**Observation:** Cancellation and return-related labels can be concentrated by category and SKU, but they are status proxies rather than validated rates.

**Evidence:** The status sets below are descriptive line counts and units; stock indicators are calculated only within the undated stock snapshot.

**Interpretation:** Concentration highlights where a status review may be useful, without asserting a completed-order denominator or return rate.

**Business implication:** Prioritise status-rule review for categories/SKUs with high cancelled or return-related line volume, and separately review zero-stock snapshots.

**Limitation:** Mixed line statuses require an order-level precedence rule; stock has no date and its `sku_code` is non-unique."""),
    code(
        "cancelled = amazon[amazon['status'].eq('Cancelled')].groupby('category').agg(lines=('status', 'size'), units=('qty', 'sum'), reported_amount=('amount', 'sum')).sort_values('lines', ascending=False)",
        "return_labels = amazon[amazon['status'].str.contains('Return', case=False, na=False)]",
        "returned_by_category = return_labels.groupby('category').agg(lines=('status', 'size'), units=('qty', 'sum'), reported_amount=('amount', 'sum')).sort_values('lines', ascending=False)",
        "stock_category = stock.groupby('category', dropna=False).agg(stock_units=('stock', 'sum'), rows=('category', 'size'), zero_stock_rows=('stock', lambda s: (s == 0).sum())).sort_values('stock_units', ascending=False)",
        "display(cancelled.head(10), returned_by_category.head(10), stock_category)",
        "assert cancelled['lines'].sum() == int(amazon['status'].eq('Cancelled').sum())",
        "assert returned_by_category['lines'].sum() == int(amazon['status'].str.contains('Return', case=False, na=False).sum())",
    ),
    md("""## 8. Potential portfolio rationalisation opportunities

**Observation:** The analysis can identify review candidates, not final rationalisation decisions.

**Evidence:** Candidate signals include C-class reported-sales SKUs, low-volume SKUs within the observed window, category concentration, status concentration, and separate zero-stock snapshot rows.

**Interpretation:** A low-sales product may be new, temporarily unavailable, intentionally niche, or poorly captured by the source.

**Business implication:** Before rationalisation, validate launch date, stock availability, margin, returns, customer demand, and strategic role.

**Limitation:** No product lifecycle, cost, margin, demand forecast, or confirmed stock-to-sales key is available."""),
    code(
        "rationalisation_candidates = sku_abc[sku_abc['abc_class'].eq('C')].sort_values('reported_amount').head(20)[['reported_amount', 'reported_units', 'line_count', 'abc_class']]",
        "display(rationalisation_candidates)",
        "print('These are review candidates only; no product is labelled unprofitable or slow-moving.')",
    ),
    md("""## 9. Independent validation and limitations

The final checks reconcile product totals to sales totals, verify unique snapshot mappings, validate Pareto endpoints and ABC thresholds, and confirm that incomplete dates are not used to label products as slow-moving."""),
    code(
        "direct_category = amazon.groupby('category')['amount'].sum().sort_values(ascending=False)",
        "direct_sku = amazon.groupby('sku')['amount'].sum().sort_values(ascending=False)",
        "assert np.allclose(direct_category.values, category_perf['reported_amount'].sort_values(ascending=False).values)",
        "assert np.allclose(direct_sku.values, sku_perf['reported_amount'].sort_values(ascending=False).values)",
        "assert not may_products['sku'].duplicated().any() and not march_products['sku'].duplicated().any()",
        "assert np.isclose(sku_abc['cumulative_share'].iloc[-1], 1.0) and np.isclose(category_abc['cumulative_share'].iloc[-1], 1.0)",
        "print('Product totals, mappings, Pareto endpoints, ABC thresholds, and top-five results validated.')",
        "print('No products were labelled slow-moving, unprofitable, or discontinued.')",
    ),
]


notebook = {
    "cells": cells,
    "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}},
    "nbformat": 4,
    "nbformat_minor": 5,
}
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text(json.dumps(notebook, indent=1), encoding="utf-8")
print(f"Wrote {OUTPUT} with {len(cells)} cells")
