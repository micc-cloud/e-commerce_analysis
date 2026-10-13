import csv
import unittest
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CLEANED = ROOT / "data" / "cleaned"


def read_csv(name):
    with (CLEANED / name).open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class PredictiveFeasibilityTests(unittest.TestCase):
    def test_phase_stops_without_predictive_notebook(self):
        self.assertTrue((ROOT / "reports" / "predictive_feasibility.md").exists())
        self.assertTrue((ROOT / "reports" / "validation_reports" / "phase_9_validation.md").exists())
        self.assertFalse((ROOT / "notebooks" / "08_predictive_analysis.ipynb").exists())

    def test_amazon_history_and_order_status_counts(self):
        rows = read_csv("amazon_sale_report_cleaned.csv")
        frame = pd.DataFrame(rows)
        dates = pd.to_datetime(frame["date"], errors="coerce")
        self.assertEqual(len(rows), 128969)
        self.assertEqual(dates.dt.date.nunique(), 91)
        self.assertEqual(dates.min().strftime("%Y-%m-%d"), "2022-03-31")
        self.assertEqual(dates.max().strftime("%Y-%m-%d"), "2022-06-29")
        order_status = frame.groupby("order_id")["status"].agg(lambda values: set(values))
        cancelled = order_status.map(lambda values: "Cancelled" in values).sum()
        returned = order_status.map(lambda values: any("Return" in value for value in values)).sum()
        self.assertEqual(order_status.size, 120378)
        self.assertEqual(cancelled, 17185)
        self.assertEqual(returned, 1981)

    def test_outcome_and_post_outcome_fields_are_present(self):
        columns = set(read_csv("amazon_sale_report_cleaned.csv")[0])
        self.assertTrue({"status", "courier_status", "amount"}.issubset(columns))
        self.assertFalse({"order_created_at", "cancelled_at", "returned_at", "delivered_at"}.intersection(columns))

    def test_profit_target_support_is_absent(self):
        columns = set(read_csv("amazon_sale_report_cleaned.csv")[0])
        unsupported = {"cogs", "cost", "platform_fee", "shipping_cost", "tax_amount", "refund_amount"}
        self.assertFalse(unsupported.intersection(columns))


if __name__ == "__main__":
    unittest.main()
