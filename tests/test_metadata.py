import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import pandas as pd

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
)

from metadata import format_date, get_best_times, get_latest_times, get_metadata

RACE_ROWS = [
    {
        "City": "Hanoi",
        "Gender": "M",
        "Name": "Runner A",
        "Country": "VNM",
        "Time": "03:30:00",
        "Date": pd.Timestamp("2025-01-01"),
        "Year": 2025,
    },
    {
        "City": "Hanoi",
        "Gender": "M",
        "Name": "Runner B",
        "Country": "USA",
        "Time": "03:10:00",
        "Date": pd.Timestamp("2026-01-01"),
        "Year": 2026,
    },
    {
        "City": "Hanoi",
        "Gender": "F",
        "Name": "Runner C",
        "Country": "USA",
        "Time": "03:45:00",
        "Date": pd.Timestamp("2025-06-01"),
        "Year": 2025,
    },
]


class FormatDateTests(unittest.TestCase):
    def test_formats_datetime_series(self) -> None:
        result = format_date(pd.to_datetime(pd.Series(["2026-01-05"])))
        assert result is not None
        self.assertEqual(result.iloc[0], "2026-01-05")

    def test_non_datetime_series_returns_none(self) -> None:
        self.assertIsNone(format_date(pd.Series(["not-a-date"])))


class GetMetadataTests(unittest.TestCase):
    def test_writes_counts_per_city(self) -> None:
        df = pd.DataFrame(RACE_ROWS)
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "metadata.json"
            with mock.patch("metadata.get_country_codes", return_value={"Hanoi": "vn"}):
                get_metadata(df, str(out_path))

            rows = json.loads(out_path.read_text())
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["City"], "Hanoi")
            self.assertEqual(rows[0]["People Count"], 3)
            self.assertEqual(rows[0]["Country Count"], 2)
            self.assertEqual(rows[0]["Country"], "vn")


class GetLatestTimesTests(unittest.TestCase):
    def test_keeps_most_recent_row_per_city_and_gender(self) -> None:
        df = pd.DataFrame(RACE_ROWS)
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "latest.json"
            with mock.patch("metadata.get_athlete_country", new=lambda c: c.lower()):
                get_latest_times(df, str(out_path))

            rows = json.loads(out_path.read_text())
            male_rows = [r for r in rows if r["Gender"] == "M"]
            self.assertEqual(len(male_rows), 1)
            self.assertEqual(male_rows[0]["Name"], "Runner B")


class GetBestTimesTests(unittest.TestCase):
    def test_keeps_fastest_row_per_city_and_gender(self) -> None:
        df = pd.DataFrame(RACE_ROWS)
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "best.json"
            with mock.patch("metadata.get_athlete_country", new=lambda c: c.lower()):
                get_best_times(df, str(out_path))

            rows = json.loads(out_path.read_text())
            male_rows = [r for r in rows if r["Gender"] == "M"]
            self.assertEqual(len(male_rows), 1)
            self.assertEqual(male_rows[0]["Name"], "Runner B")


if __name__ == "__main__":
    unittest.main()
