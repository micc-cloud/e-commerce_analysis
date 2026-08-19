import unittest
from pathlib import Path

import duckdb
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CLEANED = ROOT / "data" / "cleaned"


class Remediation02Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = duckdb.connect(":memory:")
        for path in sorted((ROOT / "sql").glob("*.sql")):
            cls.db.execute(path.read_text(encoding="utf-8"))
        cls.amazon = pd.read_csv(CLEANED / "amazon_sale_report_cleaned.csv")
        cls.international = pd.read_csv(CLEANED / "international_sale_report_cleaned.csv")
        cls.stock = pd.read_csv(CLEANED / "sale_report_cleaned.csv")

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_eda_disclosures_are_present(self):
        text = (ROOT / "notebooks/02_eda.ipynb").read_text(encoding="utf-8")
        self.assertIn("91 observed dates", text)
        self.assertIn("partial boundary months", text)
        self.assertIn("missing amount values", text)
        self.assertIn("status proxies under an analytical convention", text)
        self.assertIn("currency is not supplied", text)

    def test_sql_reconciles_six_independent_pandas_totals(self):
        checks = [
            ("SELECT COUNT(*) FROM amazon_sales", len(self.amazon)),
            ("SELECT COUNT(DISTINCT order_id) FROM amazon_sales", self.amazon["order_id"].nunique()),
            ("SELECT SUM(CAST(amount AS DOUBLE)) FROM amazon_sales", self.amazon["amount"].sum()),
            ("SELECT SUM(CAST(qty AS DOUBLE)) FROM amazon_sales", self.amazon["qty"].sum()),
            ("SELECT SUM(CAST(gross_amt AS DOUBLE)) FROM international_sales", self.international["gross_amt"].sum()),
            ("SELECT SUM(CAST(stock AS DOUBLE)) FROM stock_snapshot", self.stock["stock"].sum()),
        ]
        for query, pandas_value in checks:
            sql_value = self.db.execute(query).fetchone()[0]
            self.assertAlmostEqual(float(sql_value), float(pandas_value), places=6, msg=query)

    def test_sql_exposes_amount_coverage_and_zero_counts(self):
        row = self.db.execute(
            "SELECT amount_lines, line_count, amount_coverage_pct, zero_amount_lines, zero_quantity_lines "
            "FROM amazon_monthly_sales WHERE sales_month = DATE '2022-04-01'"
        ).fetchone()
        april = self.amazon[pd.to_datetime(self.amazon["date"]).dt.to_period("M") == "2022-04"]
        self.assertEqual(row[0], int(april["amount"].notna().sum()))
        self.assertEqual(row[1], len(april))
        self.assertAlmostEqual(row[2], 100 * april["amount"].notna().mean(), places=6)
        self.assertEqual(row[3], int((april["amount"] == 0).sum()))
        self.assertEqual(row[4], int((april["qty"] == 0).sum()))

    def test_candidate_product_join_does_not_multiply_rows(self):
        base = self.db.execute("SELECT COUNT(*) FROM amazon_sales").fetchone()[0]
        joined = self.db.execute(
            "SELECT COUNT(*) FROM amazon_sales a LEFT JOIN may_product_prices p ON a.sku = p.sku"
        ).fetchone()[0]
        self.assertEqual(base, joined)

    def test_unsupported_views_and_unsafe_cost_joins_are_absent(self):
        names = {
            row[0]
            for row in self.db.execute(
                "SELECT table_name FROM duckdb_tables() UNION ALL SELECT view_name FROM duckdb_views()"
            ).fetchall()
        }
        self.assertFalse(any(term in name.lower() for name in names for term in ("profit", "margin", "customer")))
        sql_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in [ROOT / "sql/02_sales_analysis.sql", ROOT / "sql/03_product_analysis.sql", ROOT / "sql/04_operations_analysis.sql"]
        ).lower()
        self.assertNotIn("join warehouse_rates", sql_text)


if __name__ == "__main__":
    unittest.main()
