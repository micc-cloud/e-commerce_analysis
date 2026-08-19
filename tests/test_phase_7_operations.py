from pathlib import Path
import unittest

import pandas as pd

from src.status_scope import add_status_scope


ROOT = Path(__file__).resolve().parents[1]


class Phase7OperationsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amazon = pd.read_csv(ROOT / "data/cleaned/amazon_sale_report_cleaned.csv", low_memory=False)
        cls.amazon = add_status_scope(cls.amazon)
        cls.orders = cls.amazon.groupby("order_id").agg(
            status=("status", "first"),
            status_count=("status", "nunique"),
            status_values=("status", lambda values: tuple(sorted(values.dropna().unique()))),
        ).reset_index()

    def test_order_level_deduplication_and_mixed_statuses(self):
        self.assertEqual(len(self.orders), self.amazon["order_id"].nunique())
        self.assertEqual(int(self.orders["status_count"].gt(1).sum()), 0)

    def test_status_totals_reconcile(self):
        self.assertEqual(int(self.amazon.groupby("status").size().sum()), len(self.amazon))
        self.assertEqual(int(self.orders.groupby("status").size().sum()), len(self.orders))
        self.assertEqual(int(self.orders["status"].eq("Cancelled").sum()), 17185)
        self.assertEqual(int(self.orders["status"].eq("Shipped - Delivered to Buyer").sum()), 26566)

    def test_rates_use_distinct_order_denominator(self):
        denominator = len(self.orders)
        cancellation = self.orders["status"].eq("Cancelled").sum() / denominator
        delivered = self.orders["status"].eq("Shipped - Delivered to Buyer").sum() / denominator
        self.assertAlmostEqual(cancellation, 17185 / 120378, places=10)
        self.assertAlmostEqual(delivered, 26566 / 120378, places=10)
        self.assertGreaterEqual(cancellation, 0)
        self.assertLessEqual(delivered, 1)

    def test_fulfilment_and_channel_order_totals_reconcile(self):
        self.assertEqual(self.amazon.groupby("fulfilment")["order_id"].nunique().sum(), 120378)
        self.assertEqual(self.amazon.groupby("sales_channel")["order_id"].nunique().sum(), 120378)

    def test_small_sample_flag_is_present(self):
        channel_orders = self.amazon.groupby("sales_channel")["order_id"].nunique()
        self.assertLess(channel_orders["Non-Amazon"], 1000)


if __name__ == "__main__":
    unittest.main()
