from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "notebooks" / "06_operations_analytics.ipynb"


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code(*lines):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [line + "\n" for line in lines]}


cells = [
    md("""# Phase 7: Operations Analytics

## Objective

Evaluate Amazon order-status and fulfilment indicators using explicit order-level denominators and descriptive status proxies.

**Scope control:** No delivery duration, SLA, courier-speed ranking, true cancellation rate, true return rate, or warehouse allocation is calculated."""),
    code(
        "from pathlib import Path",
        "import numpy as np",
        "import pandas as pd",
        "import matplotlib.pyplot as plt",
        "try:",
        "    from IPython.display import display",
        "except ImportError:",
        "    def display(*objects):",
        "        for obj in objects: print(obj)",
        "ROOT = Path.cwd()",
        "if not (ROOT / 'data').exists(): ROOT = ROOT.parent",
        "from src.status_scope import add_status_scope",
        "amazon = pd.read_csv(ROOT / 'data/cleaned/amazon_sale_report_cleaned.csv', low_memory=False)",
        "amazon = add_status_scope(amazon)",
        "warehouse = pd.read_csv(ROOT / 'data/cleaned/cloud_warehouse_compersion_chart_cleaned.csv', low_memory=False)",
        "print('Amazon lines:', len(amazon), '| distinct orders:', amazon['order_id'].nunique())",
    ),
    md("""## 1. Grain, order-level status, and mixed-status checks

**Observation:** Amazon rows are line grain, while operational rates use distinct order IDs.

**Evidence:** An order-status table is built by grouping each order and retaining status values, fulfilment values, channel values, and courier values.

**Interpretation:** The table prevents line duplication from inflating order-level rates and checks whether an order has multiple status values.

**Business implication:** Rates can be reproduced from the order-level table and their denominator is explicit.

**Limitation:** Status labels are source proxies; no business-approved lifecycle precedence rule exists."""),
    code(
        "order_status = amazon.groupby('order_id').agg(status=('status', 'first'), status_values=('status', lambda values: tuple(sorted(values.dropna().unique())),), status_count=('status', 'nunique'), fulfilment=('fulfilment', 'first'), channel=('sales_channel', 'first'), courier_status=('courier_status', 'first')).reset_index()",
        "order_status['has_cancelled_status'] = order_status['status_values'].apply(lambda values: any(str(v).lower() == 'cancelled' for v in values))",
        "order_status['has_return_status'] = order_status['status_values'].apply(lambda values: any('return' in str(v).lower() for v in values))",
        "order_status['has_shipped_status'] = order_status['status_values'].apply(lambda values: any(str(v).lower().startswith('shipped') for v in values))",
        "order_status['has_delivered_status_proxy'] = order_status['status_values'].apply(lambda values: 'Shipped - Delivered to Buyer' in values)",
        "print('Orders:', len(order_status), '| mixed-status orders:', int(order_status['status_count'].gt(1).sum()))",
        "print('Mixed fulfilment orders:', int(amazon.groupby('order_id')['fulfilment'].nunique().gt(1).sum()), '| mixed channel orders:', int(amazon.groupby('order_id')['sales_channel'].nunique().gt(1).sum()))",
        "assert len(order_status) == amazon['order_id'].nunique()",
        "assert order_status['status_count'].le(1).all()",
    ),
    md("""## 2. Order-status distribution and explicit rate definitions

**Observation:** Status distribution is shown at both line and distinct-order grain.

**Evidence:** Every rate uses the denominator `COUNT(DISTINCT order_id)` across the Amazon reported source: `120,378` orders.

**Definitions:**

- Cancellation status proxy = orders with exact `Cancelled` status / all distinct orders.
- Return status proxy = orders with any status containing `Return` / all distinct orders.
- Shipped status proxy = orders with any status beginning `Shipped` / all distinct orders.
- Delivered status proxy = orders with exact `Shipped - Delivered to Buyer` / all distinct orders.

**Limitation:** These are status proxies, not validated business rates."""),
    code(
        "line_status = amazon.groupby('status', dropna=False).agg(line_count=('status', 'size'), distinct_orders=('order_id', 'nunique')).sort_values('line_count', ascending=False)",
        "order_status_distribution = order_status.groupby('status', dropna=False).size().to_frame('distinct_orders').sort_values('distinct_orders', ascending=False)",
        "denominator_orders = len(order_status)",
        "rates = pd.Series({'cancellation_status_proxy_rate': order_status['has_cancelled_status'].mean(), 'return_status_proxy_rate': order_status['has_return_status'].mean(), 'shipped_status_proxy_rate': order_status['has_shipped_status'].mean(), 'delivered_status_proxy_rate': order_status['has_delivered_status_proxy'].mean()})",
        "display(line_status, order_status_distribution, rates.to_frame('rate'))",
        "print('Rate denominator: distinct Amazon order IDs =', denominator_orders)",
        "assert line_status['line_count'].sum() == len(amazon)",
        "assert order_status_distribution['distinct_orders'].sum() == denominator_orders",
        "assert ((rates >= 0) & (rates <= 1)).all()",
    ),
    md("""## 3. Fulfilment method and courier status

**Observation:** Fulfilment and courier labels are available, but timestamps are not.

**Evidence:** The tables show lines and distinct orders by `fulfilment`, `fulfilled_by`, and `courier_status`.

**Interpretation:** These are operational mix indicators, not delivery-speed or SLA measures.

**Business implication:** Use the mix to identify process-review areas and missing-data priorities.

**Limitation:** No order date-to-delivery date duration can be calculated, and courier labels do not establish speed."""),
    code(
        "fulfilment_lines = amazon.groupby('fulfilment', dropna=False).agg(line_count=('fulfilment','size'), distinct_orders=('order_id','nunique')).sort_values('distinct_orders', ascending=False)",
        "fulfilled_by_lines = amazon.groupby('fulfilled_by', dropna=False).agg(line_count=('fulfilled_by','size'), distinct_orders=('order_id','nunique')).sort_values('distinct_orders', ascending=False)",
        "courier_lines = amazon.groupby('courier_status', dropna=False).agg(line_count=('courier_status','size'), distinct_orders=('order_id','nunique')).sort_values('distinct_orders', ascending=False)",
        "display(fulfilment_lines, fulfilled_by_lines, courier_lines)",
        "assert fulfilment_lines['line_count'].sum() == len(amazon)",
        "assert courier_lines['line_count'].sum() == len(amazon)",
    ),
    md("""## 4. Platform and category operational differences

**Observation:** Operational proxy rates can be compared by channel and category with sample-size flags.

**Evidence:** Group denominators are distinct orders within each channel/category; `MIN_GROUP_ORDERS = 1,000` is an analytical sufficiency flag, not a business rule.

**Interpretation:** Differences may reflect product mix, status composition, or sample size; no causal ranking is made.

**Business implication:** Prioritise groups with enough observations for operational review and treat small groups as directional only.

**Limitation:** The Non-Amazon channel has a much smaller sample than Amazon.in, and category populations differ materially."""),
    code(
        "MIN_GROUP_ORDERS = 1000",
        "def operational_rates(frame, group_col):",
        "    grouped = frame.groupby(group_col, dropna=False)",
        "    result = grouped.agg(distinct_orders=('order_id','nunique'), lines=('order_id','size'), cancelled_orders=('has_cancelled_status','sum'), return_orders=('has_return_status','sum'), shipped_orders=('has_shipped_status','sum'), delivered_orders=('has_delivered_status_proxy','sum'))",
        "    result['cancellation_status_proxy_rate'] = result['cancelled_orders'] / result['distinct_orders']",
        "    result['return_status_proxy_rate'] = result['return_orders'] / result['distinct_orders']",
        "    result['shipped_status_proxy_rate'] = result['shipped_orders'] / result['distinct_orders']",
        "    result['delivered_status_proxy_rate'] = result['delivered_orders'] / result['distinct_orders']",
        "    result['sample_flag'] = np.where(result['distinct_orders'] >= MIN_GROUP_ORDERS, 'sufficient_for_descriptive_comparison', 'small_sample_review_only')",
        "    return result.sort_values('distinct_orders', ascending=False)",
        "platform_operations = operational_rates(order_status, 'channel')",
        "category_order_status = order_status.merge(amazon[['order_id','category']].drop_duplicates('order_id'), on='order_id', how='left')",
        "category_operations = operational_rates(category_order_status, 'category')",
        "display(platform_operations, category_operations)",
        "assert platform_operations['distinct_orders'].sum() == denominator_orders",
        "assert category_operations['distinct_orders'].sum() == denominator_orders",
    ),
    md("""## 5. High-risk review candidates

**Observation:** Categories and SKUs can be flagged for operational review using status-proxy rates and minimum order observations.

**Evidence:** Candidates are descriptive groups with at least 100 distinct orders; no causal risk score or business loss estimate is created.

**Interpretation:** A high proxy rate may reflect data/status process differences or product mix rather than operational failure.

**Business implication:** Review candidate groups with source owners before action.

**Limitation:** SKU-level rates are not stable for very small samples and no financial impact is available."""),
    code(
        "order_with_sku = order_status.merge(amazon[['order_id','sku']].drop_duplicates('order_id'), on='order_id', how='left')",
        "sku_operations = operational_rates(order_with_sku, 'sku')",
        "sku_operations['review_candidate'] = (sku_operations['distinct_orders'] >= 100) & ((sku_operations['cancellation_status_proxy_rate'] > rates['cancellation_status_proxy_rate']) | (sku_operations['return_status_proxy_rate'] > rates['return_status_proxy_rate']))",
        "category_review = category_operations[(category_operations['distinct_orders'] >= 100) & (category_operations['cancellation_status_proxy_rate'] > rates['cancellation_status_proxy_rate'])].copy()",
        "sku_review = sku_operations[sku_operations['review_candidate']].sort_values(['return_status_proxy_rate','cancellation_status_proxy_rate'], ascending=False).head(20)",
        "display(category_review, sku_review)",
        "print('Review candidates are not labelled high-risk operational failures.')",
    ),
    md("""## 6. Warehouse comparison and exclusions

**Observation:** Warehouse provider prices are available as standalone reference rows but cannot be linked to Amazon orders or fulfilment outcomes.

**Evidence:** The warehouse table has no order ID, SKU, date, or common transaction key.

**Interpretation:** A provider-rate comparison may be descriptive, but it cannot explain order-level performance.

**Business implication:** Keep warehouse comparison outside order fulfilment ranking until a transaction-level linkage exists.

**Explicit exclusions:** delivery duration, on-time delivery, SLA compliance, courier speed ranking, true cancellation rate, true return rate, warehouse-attributed performance, and causal platform/category claims."""),
    code(
        "display(warehouse)",
        "assert not {'order_id', 'sku', 'date'}.issubset(warehouse.columns)",
        "print('Warehouse data is not joined to operational order records.')",
    ),
    md("""## 7. Reconciliation and limitations

The final checks reconcile line and order status totals, verify order-level deduplication, confirm denominators, examine mixed-status orders, and verify sample-size flags."""),
    code(
        "assert order_status['status_count'].eq(1).all()",
        "assert int(order_status['has_cancelled_status'].sum()) == int(order_status_distribution.loc['Cancelled', 'distinct_orders'])",
        "assert int(order_status['has_delivered_status_proxy'].sum()) == int(order_status_distribution.loc['Shipped - Delivered to Buyer', 'distinct_orders'])",
        "assert platform_operations['sample_flag'].isin({'sufficient_for_descriptive_comparison','small_sample_review_only'}).all()",
        "assert category_operations['sample_flag'].isin({'sufficient_for_descriptive_comparison','small_sample_review_only'}).all()",
        "print('Operations totals, order deduplication, status denominators, mixed-status checks, and sample flags validated.')",
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
