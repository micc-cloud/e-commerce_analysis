from pathlib import Path
import unittest

import pandas as pd

from src.status_scope import add_status_scope


ROOT = Path(__file__).resolve().parents[1]


class Phase5ProductTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amazon = pd.read_csv(ROOT / "data/cleaned/amazon_sale_report_cleaned.csv", low_memory=False)
        cls.amazon["amount"] = pd.to_numeric(cls.amazon["amount"], errors="coerce")
        cls.amazon["qty"] = pd.to_numeric(cls.amazon["qty"], errors="coerce")
        cls.amazon = add_status_scope(cls.amazon)
        cls.delivered = cls.amazon[cls.amazon["is_delivered_status_proxy"]]
        cls.may = pd.read_csv(ROOT / "data/cleaned/may_2022_cleaned.csv", low_memory=False)
        cls.march = pd.read_csv(ROOT / "data/cleaned/p_l_march_2021_cleaned.csv", low_memory=False)
        cls.stock = pd.read_csv(ROOT / "data/cleaned/sale_report_cleaned.csv", low_memory=False)

    def test_product_snapshot_skus_are_unique(self):
        self.assertFalse(self.may["sku"].duplicated().any())
        self.assertFalse(self.march["sku"].duplicated().any())

    def test_amazon_sku_mapping_is_within_source_consistent(self):
        mapping = self.amazon.groupby("sku")["category"].nunique()
        styles = self.amazon.groupby("sku")["style"].nunique()
        sizes = self.amazon.groupby("sku")["size"].nunique()
        self.assertEqual(int((mapping > 1).sum()), 0)
        self.assertEqual(int((styles > 1).sum()), 0)
        self.assertEqual(int((sizes > 1).sum()), 0)

    def test_product_totals_reconcile_to_sales(self):
        total = self.amazon["amount"].sum()
        self.assertAlmostEqual(self.amazon.groupby("sku")["amount"].sum().sum(), total, places=2)
        self.assertAlmostEqual(self.amazon.groupby("category")["amount"].sum().sum(), total, places=2)
        self.assertAlmostEqual(self.amazon.groupby("sku")["qty"].sum().sum(), self.amazon["qty"].sum(), places=2)

    def test_delivered_scope_product_totals_reconcile(self):
        total = self.delivered["amount"].sum()
        self.assertAlmostEqual(self.delivered.groupby("sku")["amount"].sum().sum(), total, places=2)
        self.assertAlmostEqual(self.delivered.groupby("category")["amount"].sum().sum(), total, places=2)

    def test_pareto_and_abc_thresholds(self):
        values = self.amazon.groupby("sku")["amount"].sum().sort_values(ascending=False)
        cumulative = values.cumsum() / values.sum()
        self.assertTrue(cumulative.is_monotonic_increasing)
        self.assertAlmostEqual(cumulative.iloc[-1], 1.0, places=10)
        abc = pd.Series("C", index=cumulative.index)
        abc[cumulative <= 0.80] = "A"
        abc[(cumulative > 0.80) & (cumulative <= 0.95)] = "B"
        self.assertTrue(set(abc).issubset({"A", "B", "C"}))
        self.assertEqual(abc.iloc[0], "A")

    def test_no_exact_amazon_to_may_sku_match_and_stock_key_warning(self):
        self.assertEqual(int(self.amazon["sku"].isin(self.may["sku"]).sum()), 0)
        duplicate_keys = self.stock.dropna(subset=["sku_code"]).groupby("sku_code").size().gt(1).sum()
        self.assertEqual(int(duplicate_keys), 5)


if __name__ == "__main__":
    unittest.main()
