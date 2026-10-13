from pathlib import Path
import unittest

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "amazon_sale_report_cleaned.csv": {"order_id", "date", "status", "sku", "qty", "amount", "currency"},
    "international_sale_report_cleaned.csv": {"date", "months", "customer", "sku", "pcs", "rate", "gross_amt"},
    "may_2022_cleaned.csv": {"sku", "tp", "amazon_mrp"},
    "p_l_march_2021_cleaned.csv": {"sku", "tp_1", "tp_2", "amazon_mrp"},
    "sale_report_cleaned.csv": {"sku_code", "stock"},
    "cloud_warehouse_compersion_chart_cleaned.csv": {"cost_head", "shiprocket_price_per_unit", "increff_price_per_unit"},
    "expense_iigf_cleaned.csv": {"transaction_type", "record_type", "particular", "amount"},
}


class Phase1ScopeTests(unittest.TestCase):
    def test_kpi_required_fields_exist(self):
        for filename, fields in EXPECTED.items():
            frame = pd.read_csv(ROOT / "data" / "cleaned" / filename, nrows=0)
            self.assertTrue(fields.issubset(frame.columns), filename)

    def test_phase_1_documents_exist(self):
        for path in ["docs/data_dictionary.md", "docs/kpi_definition.md", "docs/business_scope.md", "images/data_model.svg", "reports/validation_reports/phase_1_validation.md"]:
            self.assertTrue((ROOT / path).exists(), path)

    def test_kpi_formula_field_references_exist(self):
        formulas = {
            "amazon_gross_sales": ("amazon_sale_report_cleaned.csv", {"amount"}),
            "international_gross_sales": ("international_sale_report_cleaned.csv", {"gross_amt"}),
            "amazon_orders": ("amazon_sale_report_cleaned.csv", {"order_id"}),
            "amazon_units": ("amazon_sale_report_cleaned.csv", {"qty"}),
            "international_units": ("international_sale_report_cleaned.csv", {"pcs"}),
            "amazon_asp": ("amazon_sale_report_cleaned.csv", {"amount", "qty"}),
            "international_asp": ("international_sale_report_cleaned.csv", {"gross_amt", "pcs"}),
            "amazon_cancellation_rate": ("amazon_sale_report_cleaned.csv", {"order_id", "status"}),
            "stock_snapshot": ("sale_report_cleaned.csv", {"sku_code", "stock"}),
        }
        for name, (filename, fields) in formulas.items():
            columns = set(pd.read_csv(ROOT / "data" / "cleaned" / filename, nrows=0).columns)
            self.assertTrue(fields.issubset(columns), name)

    def test_unsupported_customer_fields_are_not_invented(self):
        dictionary = (ROOT / "docs" / "data_dictionary.md").read_text(encoding="utf-8")
        self.assertNotIn("customer_id", dictionary)
        self.assertNotIn("customer_lifetime_value", dictionary)


if __name__ == "__main__":
    unittest.main()
