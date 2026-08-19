import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


class Phase5RevalidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amazon = pd.read_csv(ROOT / "data/cleaned/amazon_sale_report_cleaned.csv")
        cls.may = pd.read_csv(ROOT / "data/cleaned/may_2022_cleaned.csv")
        cls.march = pd.read_csv(ROOT / "data/cleaned/p_l_march_2021_cleaned.csv")
        cls.stock = pd.read_csv(ROOT / "data/cleaned/sale_report_cleaned.csv")
        cls.delivered = cls.amazon[cls.amazon["status"].eq("Shipped - Delivered to Buyer")]

    def test_notebook_labels_scope_metric_and_exclusions(self):
        text = (ROOT / "notebooks/04_product_analytics.ipynb").read_text(encoding="utf-8")
        for phrase in [
            "delivered_status_proxy",
            "reported gross amount",
            "Candidate Amazon-to-May match rate",
            "amount coverage",
            "B2B",
            "No products were labelled slow-moving, unprofitable, or discontinued",
        ]:
            self.assertIn(phrase, text)

    def test_mapping_coverage_and_uniqueness(self):
        self.assertFalse(self.may["sku"].duplicated().any())
        self.assertFalse(self.march["sku"].duplicated().any())
        self.assertEqual(int(self.delivered["sku"].isin(self.may["sku"]).sum()), 0)
        mapping = self.amazon.groupby("sku").agg(
            categories=("category", "nunique"), styles=("style", "nunique"), sizes=("size", "nunique")
        )
        self.assertEqual(int((mapping > 1).any(axis=1).sum()), 0)

    def test_product_totals_reconcile_to_phase4_scope(self):
        total_amount = self.delivered["amount"].sum()
        total_units = self.delivered["qty"].sum()
        total_orders = self.delivered["order_id"].nunique()
        self.assertAlmostEqual(self.delivered.groupby("sku")["amount"].sum().sum(), total_amount, places=2)
        self.assertAlmostEqual(self.delivered.groupby("category")["amount"].sum().sum(), total_amount, places=2)
        self.assertAlmostEqual(self.delivered.groupby("sku")["qty"].sum().sum(), total_units, places=2)
        self.assertEqual(self.delivered["order_id"].nunique(), total_orders)

    def test_reported_gross_amount_abc_is_monotonic_and_complete(self):
        values = self.delivered.groupby("sku")["amount"].sum().sort_values(ascending=False)
        cumulative = values.cumsum() / values.sum()
        self.assertTrue(cumulative.is_monotonic_increasing)
        self.assertAlmostEqual(cumulative.iloc[-1], 1.0, places=10)
        abc = pd.Series("C", index=cumulative.index)
        abc[cumulative <= 0.80] = "A"
        abc[(cumulative > 0.80) & (cumulative <= 0.95)] = "B"
        self.assertEqual(abc.value_counts().to_dict(), {"C": 1544, "B": 1453, "A": 1433})

    def test_status_b2b_and_amount_coverage_are_source_local(self):
        self.assertEqual(int(self.amazon["amount"].isna().sum()), 7792)
        self.assertAlmostEqual(self.delivered["amount"].notna().mean(), 0.9997219229, places=8)
        cancelled = self.amazon[self.amazon["status"].eq("Cancelled")]
        returned = self.amazon[self.amazon["status"].str.contains("Return", na=False)]
        self.assertGreater(len(cancelled), 0)
        self.assertGreater(len(returned), 0)
        self.assertEqual(set(self.delivered["b2b"].dropna().unique()), {False, True})

    def test_stock_is_not_used_as_a_sales_join(self):
        duplicate_keys = self.stock.dropna(subset=["sku_code"]).groupby("sku_code").size().gt(1).sum()
        self.assertEqual(int(duplicate_keys), 5)
        self.assertNotIn("amount", self.stock.columns)


if __name__ == "__main__":
    unittest.main()
