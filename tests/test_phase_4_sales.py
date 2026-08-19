from pathlib import Path
import unittest

import duckdb
import pandas as pd

from src.status_scope import DELIVERED_STATUS, add_status_scope


ROOT = Path(__file__).resolve().parents[1]


class Phase4SalesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amazon = pd.read_csv(ROOT / "data/cleaned/amazon_sale_report_cleaned.csv", low_memory=False)
        cls.amazon["amount"] = pd.to_numeric(cls.amazon["amount"], errors="coerce")
        cls.amazon["qty"] = pd.to_numeric(cls.amazon["qty"], errors="coerce")
        cls.amazon["date"] = pd.to_datetime(cls.amazon["date"], errors="coerce")
        cls.amazon = add_status_scope(cls.amazon)
        cls.db = duckdb.connect(str(ROOT / "data/processed/ecommerce.duckdb"), read_only=True)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_headlines_reconcile_to_sql(self):
        sql = self.db.execute("SELECT SUM(reported_amount), SUM(reported_units), SUM(distinct_orders) FROM amazon_monthly_sales").fetchone()
        self.assertAlmostEqual(self.amazon["amount"].sum(), sql[0], places=2)
        self.assertAlmostEqual(self.amazon["qty"].sum(), sql[1], places=2)
        self.assertEqual(self.amazon["order_id"].nunique(), sql[2])

    def test_order_counts_are_distinct(self):
        self.assertLessEqual(self.amazon["order_id"].nunique(), len(self.amazon))
        self.assertEqual(self.amazon["order_id"].nunique(), 120378)

    def test_delivered_status_proxy_is_explicit_and_reconciles_to_sql(self):
        delivered = self.amazon[self.amazon["is_delivered_status_proxy"]]
        self.assertTrue((delivered["status"] == DELIVERED_STATUS).all())
        sql = self.db.execute("SELECT SUM(reported_amount), SUM(reported_units), SUM(distinct_orders) FROM amazon_monthly_sales_scoped WHERE analysis_scope = 'delivered_status_proxy'").fetchone()
        self.assertAlmostEqual(delivered["amount"].sum(), sql[0], places=2)
        self.assertAlmostEqual(delivered["qty"].sum(), sql[1], places=2)
        self.assertEqual(delivered["order_id"].nunique(), sql[2])

    def test_amount_coverage_is_reported_by_status(self):
        coverage = self.amazon.groupby("status")["amount"].apply(lambda values: values.notna().mean())
        self.assertLess(coverage.loc["Cancelled"], 0.70)
        self.assertGreater(coverage.loc[DELIVERED_STATUS], 0.99)

    def test_partial_month_growth_is_suppressed(self):
        month = self.amazon.groupby(self.amazon["date"].dt.to_period("M"))["amount"].sum().to_frame("amount")
        month["partial"] = month.index.isin([pd.Period("2022-03"), pd.Period("2022-06")])
        previous_partial = month["partial"].shift(1, fill_value=False)
        month["comparable_mom"] = month["amount"].pct_change().where(~month["partial"] & ~previous_partial)
        self.assertTrue(pd.isna(month.loc[pd.Period("2022-04"), "comparable_mom"]))
        self.assertAlmostEqual(month.loc[pd.Period("2022-05"), "comparable_mom"], -0.090612, places=4)
        self.assertTrue(pd.isna(month.loc[pd.Period("2022-06"), "comparable_mom"]))

    def test_concentration_denominators_sum_to_one(self):
        categories = self.amazon.groupby("category")["amount"].sum()
        skus = self.amazon.dropna(subset=["sku"]).groupby("sku")["amount"].sum()
        self.assertAlmostEqual((categories / categories.sum()).sum(), 1.0, places=10)
        self.assertAlmostEqual((skus / skus.sum()).sum(), 1.0, places=10)

    def test_top_five_results_reproduce(self):
        category_top = self.amazon.groupby("category")["amount"].sum().sort_values(ascending=False).head(5)
        sku_top = self.amazon.dropna(subset=["sku"]).groupby("sku")["amount"].sum().sort_values(ascending=False).head(5)
        self.assertEqual(category_top.index.tolist(), ["Set", "kurta", "Western Dress", "Top", "Ethnic Dress"])
        self.assertEqual(sku_top.index.tolist(), ["J0230-SKD-M", "JNE3797-KR-L", "J0230-SKD-S", "JNE3797-KR-M", "JNE3797-KR-S"])


if __name__ == "__main__":
    unittest.main()
