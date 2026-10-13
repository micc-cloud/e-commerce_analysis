import unittest
from pathlib import Path

import duckdb
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


class Phase4RevalidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amazon = pd.read_csv(ROOT / "data/cleaned/amazon_sale_report_cleaned.csv")
        cls.international = pd.read_csv(ROOT / "data/cleaned/international_sale_report_cleaned.csv")
        cls.amazon["date"] = pd.to_datetime(cls.amazon["date"])
        cls.db = duckdb.connect(str(ROOT / "data/processed/ecommerce.duckdb"), read_only=True)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_notebook_contains_required_governance_disclosures(self):
        text = (ROOT / "notebooks/03_sales_analytics.ipynb").read_text(encoding="utf-8")
        for phrase in [
            "reported gross-value measures",
            "not a confirmed completed-sales definition",
            "partial boundary months",
            "missing values are retained",
            "currency is not supplied",
            "seasonal pattern claim",
        ]:
            self.assertIn(phrase, text)

    def test_headline_sql_reconciles_to_pandas(self):
        sql = self.db.execute(
            "SELECT SUM(reported_amount), SUM(reported_units), SUM(distinct_orders) FROM amazon_monthly_sales"
        ).fetchone()
        self.assertAlmostEqual(sql[0], self.amazon["amount"].sum(), places=2)
        self.assertAlmostEqual(sql[1], self.amazon["qty"].sum(), places=2)
        self.assertEqual(sql[2], self.amazon["order_id"].nunique())

    def test_delivered_proxy_reconciles_to_pandas(self):
        delivered = self.amazon[self.amazon["status"].eq("Shipped - Delivered to Buyer")]
        sql = self.db.execute(
            "SELECT SUM(reported_amount), SUM(reported_units), SUM(distinct_orders) "
            "FROM amazon_monthly_sales_scoped WHERE analysis_scope = 'delivered_status_proxy'"
        ).fetchone()
        self.assertAlmostEqual(sql[0], delivered["amount"].sum(), places=2)
        self.assertAlmostEqual(sql[1], delivered["qty"].sum(), places=2)
        self.assertEqual(sql[2], delivered["order_id"].nunique())

    def test_amount_coverage_and_boundary_month_rule(self):
        self.assertEqual(int(self.amazon["amount"].isna().sum()), 7792)
        self.assertAlmostEqual(self.amazon["amount"].notna().mean(), 0.9395823803, places=8)
        monthly = self.amazon.groupby(self.amazon["date"].dt.to_period("M"))["amount"].sum()
        partial = monthly.index.isin([pd.Period("2022-03"), pd.Period("2022-06")])
        previous_partial = pd.Series(partial, index=monthly.index).shift(1, fill_value=False).astype(bool)
        comparable = monthly.pct_change().where(~pd.Series(partial, index=monthly.index) & ~previous_partial)
        self.assertTrue(pd.isna(comparable.loc[pd.Period("2022-04")]))
        self.assertAlmostEqual(comparable.loc[pd.Period("2022-05")], -0.090612, places=4)
        self.assertTrue(pd.isna(comparable.loc[pd.Period("2022-06")]))

    def test_independent_concentration_and_top_five_results(self):
        delivered = self.amazon[self.amazon["status"].eq("Shipped - Delivered to Buyer")]
        categories = delivered.groupby("category")["amount"].sum().sort_values(ascending=False)
        skus = delivered.dropna(subset=["sku"]).groupby("sku")["amount"].sum().sort_values(ascending=False)
        self.assertAlmostEqual(categories.head(5).sum() / categories.sum(), 0.9918378902, places=8)
        self.assertAlmostEqual(skus.head(5).sum() / skus.sum(), 0.0598622098, places=8)
        self.assertEqual(skus.head(5).index.tolist(), [
            "JNE3797-KR-L", "JNE3797-KR-M", "SET183-KR-DH-M", "JNE3797-KR-S", "JNE3797-KR-XL"
        ])

    def test_international_amount_is_not_combined(self):
        self.assertNotIn("currency", self.international.columns)
        international_sql = self.db.execute("SELECT SUM(reported_gross_amount) FROM international_monthly_sales").fetchone()[0]
        self.assertAlmostEqual(international_sql, self.international["gross_amt"].sum(), places=2)


if __name__ == "__main__":
    unittest.main()
