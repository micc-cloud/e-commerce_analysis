import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


class Remediation01Tests(unittest.TestCase):
    def test_remediation_report_and_governance_documents_exist(self):
        for path in [
            "reports/validation_reports/remediation_01.md",
            "docs/kpi_definition.md",
            "docs/business_scope.md",
            "docs/data_dictionary.md",
        ]:
            self.assertTrue((ROOT / path).exists(), path)

    def test_international_dates_follow_month_column(self):
        frame = pd.read_csv(ROOT / "data/cleaned/international_sale_report_cleaned.csv")
        dates = pd.to_datetime(frame["date"], format="%m/%d/%Y", errors="coerce")
        months = pd.to_datetime(frame["months"], format="%b-%y", errors="coerce")
        self.assertEqual(int(dates.isna().sum()), 0)
        self.assertTrue((dates.dt.month == months.dt.month).all())
        self.assertTrue((dates.dt.year == months.dt.year).all())

    def test_missing_and_zero_amount_quantity_are_preserved(self):
        frame = pd.read_csv(ROOT / "data/cleaned/amazon_sale_report_cleaned.csv")
        self.assertEqual(int(frame["amount"].isna().sum()), 7792)
        self.assertEqual(int((frame["amount"] == 0).sum()), 2343)
        self.assertEqual(int((frame["qty"] == 0).sum()), 12804)

    def test_stock_duplicate_sku_is_flagged_not_deduplicated(self):
        frame = pd.read_csv(ROOT / "data/cleaned/sale_report_cleaned.csv")
        self.assertEqual(int(frame["sku_code"].duplicated(keep=False).sum()), 68)
        self.assertEqual(int(frame["sku_code"].isna().sum()), 48)

    def test_phase8_report_uses_existing_cleaned_files(self):
        report = (ROOT / "reports/validation_reports/phase_8_validation.md").read_text(encoding="utf-8")
        for filename in [
            "amazon_sale_report_cleaned.csv",
            "international_sale_report_cleaned.csv",
            "may_2022_cleaned.csv",
            "p_l_march_2021_cleaned.csv",
            "cloud_warehouse_compersion_chart_cleaned.csv",
            "sale_report_cleaned.csv",
        ]:
            self.assertIn(filename, report)
        self.assertNotIn("amazon_sales_cleaned.csv", report)


if __name__ == "__main__":
    unittest.main()
