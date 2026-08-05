from pathlib import Path
import unittest

import duckdb


ROOT = Path(__file__).resolve().parents[1]


class Phase3SqlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = duckdb.connect(":memory:")
        import os
        os.chdir(ROOT)
        for path in sorted((ROOT / "sql").glob("*.sql")):
            cls.connection.execute(path.read_text(encoding="utf-8"))

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def test_source_counts_and_distinct_orders(self):
        row = self.connection.execute("SELECT * FROM phase_3_validation WHERE table_name = 'amazon_sales'").fetchone()
        self.assertEqual(row[1], 128969)
        self.assertEqual(row[2], 120378)

    def test_product_join_does_not_multiply_amazon_rows(self):
        base = self.connection.execute("SELECT COUNT(*) FROM amazon_sales").fetchone()[0]
        joined = self.connection.execute("SELECT COUNT(*) FROM amazon_sales a LEFT JOIN may_product_prices p ON a.sku = p.sku").fetchone()[0]
        self.assertEqual(base, joined)

    def test_safe_ratio_and_monthly_window_outputs(self):
        aov = self.connection.execute("SELECT reported_value_per_distinct_order FROM amazon_monthly_sales WHERE sales_month = DATE '2022-03-01'").fetchone()[0]
        self.assertIsNotNone(aov)
        mom = self.connection.execute("SELECT amount_change_mom_pct FROM amazon_monthly_sales WHERE sales_month = DATE '2022-04-01'").fetchone()[0]
        self.assertIsNotNone(mom)

    def test_status_scoped_sales_view_is_explicit(self):
        scopes = {row[0] for row in self.connection.execute("SELECT DISTINCT analysis_scope FROM amazon_monthly_sales_scoped").fetchall()}
        self.assertEqual(scopes, {"reported_source", "delivered_status_proxy"})
        delivered = self.connection.execute("SELECT SUM(reported_amount), SUM(reported_units), SUM(distinct_orders) FROM amazon_monthly_sales_scoped WHERE analysis_scope = 'delivered_status_proxy'").fetchone()
        self.assertAlmostEqual(delivered[0], 18650815.0, places=2)
        self.assertEqual(delivered[1], 28886)
        self.assertEqual(delivered[2], 26566)

    def test_unsupported_profit_view_is_absent(self):
        names = {row[0] for row in self.connection.execute("SELECT table_name FROM duckdb_tables() UNION ALL SELECT view_name FROM duckdb_views()").fetchall()}
        self.assertFalse(any("profit" in name.lower() or "margin" in name.lower() for name in names))


if __name__ == "__main__":
    unittest.main()
