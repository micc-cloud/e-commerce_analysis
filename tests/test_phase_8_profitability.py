import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLEANED = ROOT / "data" / "cleaned"


def read_csv(name):
    with (CLEANED / name).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class ProfitabilityFeasibilityTests(unittest.TestCase):
    def test_required_reports_exist_and_analysis_is_stopped(self):
        self.assertTrue((ROOT / "reports" / "profitability_feasibility.md").exists())
        self.assertTrue((ROOT / "reports" / "validation_reports" / "phase_8_validation.md").exists())
        self.assertFalse((ROOT / "notebooks" / "07_profitability_analytics.ipynb").exists())
        self.assertFalse((ROOT / "reports" / "profitability_findings.md").exists())

    def test_sales_amount_is_incomplete_and_not_a_costed_profit_measure(self):
        rows = read_csv("amazon_sale_report_cleaned.csv")
        self.assertEqual(len(rows), 128969)
        self.assertEqual(len({row["order_id"] for row in rows}), 120378)
        self.assertEqual(sum(bool(row["amount"]) for row in rows), 121177)
        self.assertEqual(sum(not row["amount"] for row in rows), 7792)
        self.assertNotIn("cogs", rows[0])
        self.assertNotIn("refund_amount", rows[0])
        self.assertNotIn("tax_amount", rows[0])

    def test_cost_sources_cannot_join_to_sales(self):
        warehouse = read_csv("cloud_warehouse_compersion_chart_cleaned.csv")
        expense = read_csv("expense_iigf_cleaned.csv")
        self.assertEqual(len(warehouse), 4)
        self.assertNotIn("order_id", warehouse[0])
        self.assertNotIn("date", warehouse[0])
        self.assertNotIn("order_id", expense[0])
        self.assertNotIn("sku", expense[0])
        self.assertNotIn("date", expense[0])

    def test_product_snapshot_has_no_exact_amazon_sku_match(self):
        sales = read_csv("amazon_sale_report_cleaned.csv")
        products = read_csv("may_2022_cleaned.csv")
        sales_skus = {row["sku"] for row in sales if row["sku"]}
        product_skus = {row["sku"] for row in products if row["sku"]}
        self.assertEqual(len(sales_skus & product_skus), 0)

    def test_expense_summary_rows_are_present_and_not_aggregated(self):
        rows = read_csv("expense_iigf_cleaned.csv")
        self.assertTrue(any(row["record_type"] == "summary" for row in rows))
        detail_expense = sum(
            float(row["amount"])
            for row in rows
            if row["record_type"] == "detail" and row["transaction_type"] == "expense"
        )
        self.assertEqual(detail_expense, 8095.0)


if __name__ == "__main__":
    unittest.main()
