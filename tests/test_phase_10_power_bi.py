from pathlib import Path
import unittest

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "data" / "processed" / "dashboard"


class Phase10PowerBITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amazon = pd.read_csv(ROOT / "data/cleaned/amazon_sale_report_cleaned.csv", low_memory=False)
        cls.amazon["amount"] = pd.to_numeric(cls.amazon["amount"], errors="coerce")
        cls.amazon["qty"] = pd.to_numeric(cls.amazon["qty"], errors="coerce")
        cls.fact = pd.read_csv(DASHBOARD / "fact_amazon_sales.csv", low_memory=False)
        cls.date = pd.read_csv(DASHBOARD / "dim_date.csv", low_memory=False)
        cls.category = pd.read_csv(DASHBOARD / "dim_category.csv", low_memory=False)
        cls.sku = pd.read_csv(DASHBOARD / "dim_sku.csv", low_memory=False)
        cls.order_status = pd.read_csv(DASHBOARD / "dim_order_status.csv", low_memory=False)
        cls.international = pd.read_csv(DASHBOARD / "fact_international_sales.csv", low_memory=False)

    def test_dashboard_tables_exist_and_load(self):
        expected = {
            "fact_amazon_sales.csv",
            "dim_date.csv",
            "dim_category.csv",
            "dim_sku.csv",
            "dim_order_status.csv",
            "fact_international_sales.csv",
        }
        self.assertEqual(expected, {path.name for path in DASHBOARD.glob("*.csv")})
        self.assertEqual(len(self.fact), 128969)
        self.assertEqual(len(self.international), 12322)

    def test_dimension_keys_are_unique_and_relationship_keys_cover_facts(self):
        self.assertFalse(self.date["date_key"].duplicated().any())
        self.assertFalse(self.category["category_key"].duplicated().any())
        self.assertFalse(self.sku["sku_key"].duplicated().any())
        self.assertFalse(self.order_status["order_id"].duplicated().any())
        self.assertTrue(set(self.fact["date_key"]).issubset(set(self.date["date_key"])))
        self.assertTrue(set(self.fact["category"].dropna()).issubset(set(self.category["category_key"])))
        self.assertTrue(set(self.fact["sku"]).issubset(set(self.sku["sku_key"])))
        self.assertTrue(set(self.fact["order_id"]).issubset(set(self.order_status["order_id"])))

    def test_amazon_reconciliation(self):
        self.assertEqual(self.fact["order_id"].nunique(), 120378)
        self.assertEqual(self.fact["qty"].sum(), self.amazon["qty"].sum())
        self.assertAlmostEqual(self.fact["amount"].sum(), self.amazon["amount"].sum(), places=2)
        self.assertEqual(int(self.fact["amount"].notna().sum()), 121177)
        self.assertAlmostEqual(self.fact["amount_present"].mean(), 121177 / 128969, places=8)

    def test_proxy_denominators_and_mixed_status_governance(self):
        valid = self.fact[
            self.fact["is_delivered_status_proxy"].eq(True)
            & self.fact["amount"].notna()
            & self.fact["qty"].gt(0)
        ]
        self.assertEqual(len(valid), 28761)
        self.assertTrue((valid["reported_unit_price_proxy"] >= 0).all())
        self.assertEqual(int(self.order_status["mixed_status_flag"].sum()), 0)
        self.assertTrue(self.order_status["status_label"].notna().all())
        self.assertEqual(self.order_status["order_id"].nunique(), 120378)

    def test_international_fact_is_separate(self):
        self.assertNotIn("order_id", self.international.columns)
        self.assertNotIn("currency", self.international.columns)
        self.assertEqual(len(self.international), 12322)

    def test_documentation_contains_governance_and_exclusions(self):
        model = (ROOT / "docs/power_bi_model.md").read_text(encoding="utf-8")
        dax = (ROOT / "docs/dax_measures.md").read_text(encoding="utf-8")
        spec = (ROOT / "docs/dashboard_specification.md").read_text(encoding="utf-8")
        guide = (ROOT / "docs/power_bi_build_guide.md").read_text(encoding="utf-8")
        for phrase in ["Single, dimension to fact", "MIXED_STATUS_REQUIRES_RULE", "Reported Unit-Price Proxy", "Amount Coverage %"]:
            self.assertIn(phrase, model + dax + spec + guide)
        self.assertIn("Do not create measures named Profit", dax)
        self.assertIn("International currency is unspecified", spec + guide)


if __name__ == "__main__":
    unittest.main()
