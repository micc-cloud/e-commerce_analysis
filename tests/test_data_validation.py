from pathlib import Path
import unittest

import pandas as pd

from src.data_validation import EXPECTED_FILES, _candidate_key_checks, _date_summary, _status


class DataValidationTests(unittest.TestCase):
    def test_expected_cleaned_files_exist(self):
        clean_dir = Path(__file__).resolve().parents[1] / "data" / "cleaned"
        missing = [cleaned for cleaned, _ in EXPECTED_FILES.values() if not (clean_dir / cleaned).exists()]
        self.assertEqual(missing, [])

    def test_date_summary_flags_invalid_nonblank_values(self):
        result = _date_summary(pd.DataFrame({"date": ["2022-01-01", "not-a-date", None]}), "date")
        self.assertEqual(result["invalid_nonblank"], 1)
        self.assertEqual(result["missing"], 1)

    def test_candidate_key_detects_duplicate_and_null_parts(self):
        result = _candidate_key_checks(pd.DataFrame({"sku": ["A", "A", None]}), [["sku"]])[0]
        self.assertEqual(result["duplicate_rows"], 2)
        self.assertEqual(result["null_key_rows"], 1)

    def test_status_fails_for_missing_mandatory_fields(self):
        result = {"missing_expected_files": [], "files": [{"mandatory_fields_missing": ["sku"], "date_checks": [], "numeric_checks": {}, "duplicate_rows": 0, "candidate_keys": []}], "reproducibility": [], "merge_checks": []}
        self.assertEqual(_status(result), "FAIL")

    def test_international_dates_match_month_column(self):
        path = Path(__file__).resolve().parents[1] / "data" / "cleaned" / "international_sale_report_cleaned.csv"
        frame = pd.read_csv(path, dtype="string")
        dates = pd.to_datetime(frame["date"], format="%m/%d/%Y", errors="coerce")
        months = pd.to_datetime(frame["months"], format="%b-%y", errors="coerce")
        self.assertEqual(int(dates.isna().sum()), 0)
        self.assertTrue((dates.dt.month == months.dt.month).all())
        self.assertTrue((dates.dt.year == months.dt.year).all())


if __name__ == "__main__":
    unittest.main()
