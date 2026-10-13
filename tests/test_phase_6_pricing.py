from pathlib import Path
import unittest

import numpy as np
import pandas as pd

from src.status_scope import add_status_scope


ROOT = Path(__file__).resolve().parents[1]


class Phase6PricingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.amazon = pd.read_csv(ROOT / "data/cleaned/amazon_sale_report_cleaned.csv", low_memory=False)
        cls.amazon["amount"] = pd.to_numeric(cls.amazon["amount"], errors="coerce")
        cls.amazon["qty"] = pd.to_numeric(cls.amazon["qty"], errors="coerce")
        cls.amazon = add_status_scope(cls.amazon)
        cls.delivered = cls.amazon[cls.amazon["is_delivered_status_proxy"]].copy()
        cls.valid = cls.delivered[cls.delivered["currency"].eq("INR") & cls.delivered["amount"].notna() & cls.delivered["qty"].gt(0)].copy()
        cls.valid["unit_price"] = cls.valid["amount"] / cls.valid["qty"]
        cls.may = pd.read_csv(ROOT / "data/cleaned/may_2022_cleaned.csv", low_memory=False)

    def test_currency_and_price_denominators(self):
        self.assertTrue(self.valid["currency"].eq("INR").all())
        self.assertTrue((self.valid["qty"] > 0).all())
        self.assertFalse((self.valid["unit_price"] < 0).any())
        self.assertGreater(int((self.delivered["qty"] <= 0).sum()), 0)
        self.assertGreater(int(self.amazon["amount"].isna().sum()), 0)

    def test_manual_unit_price_sample(self):
        sample = self.valid[["amount", "qty", "unit_price"]].head(10)
        self.assertTrue(np.allclose(sample["unit_price"], sample["amount"] / sample["qty"]))

    def test_discount_join_is_not_supported(self):
        self.assertEqual(int(self.amazon["sku"].isin(self.may["sku"]).sum()), 0)

    def test_price_bands_are_exhaustive_and_disjoint(self):
        labels = ["[0,500)", "[500,1000)", "[1000,2000)", "[2000,inf)"]
        bands = pd.cut(self.valid["unit_price"], bins=[0, 500, 1000, 2000, np.inf], labels=labels, right=False, include_lowest=True)
        self.assertEqual(len(set(labels)), len(labels))
        self.assertTrue(bands.notna().all())
        self.assertEqual(int(bands.value_counts().sum()), len(self.valid))

    def test_snapshot_prices_are_non_negative(self):
        price_cols = [c for c in self.may.columns if c.endswith("_mrp") or c in {"mrp_old", "final_mrp_old"}]
        values = self.may[price_cols].apply(pd.to_numeric, errors="coerce")
        self.assertFalse((values < 0).any().any())

    def test_source_local_comparison_dimensions_and_sample_sizes(self):
        for column in ["b2b", "ship_state", "fulfilment"]:
            grouped = self.valid.groupby(column, dropna=False).size()
            self.assertTrue((grouped > 0).all())
        self.assertEqual(self.valid["fulfilment"].nunique(dropna=False), 1)

    def test_report_documents_proxy_and_exclusions(self):
        notebook_text = (ROOT / "notebooks/05_pricing_analytics.ipynb").read_text(encoding="utf-8")
        report_text = (ROOT / "reports/pricing_findings.md").read_text(encoding="utf-8")
        for phrase in ["reported unit-price proxy", "amount / qty", "B2B/B2C", "partial boundary", "No price elasticity"]:
            self.assertIn(phrase, notebook_text + report_text)


if __name__ == "__main__":
    unittest.main()
