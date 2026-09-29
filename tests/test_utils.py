import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
)

from utils import cache, get_athlete_country, get_country_code


class CacheTests(unittest.TestCase):
    def test_calls_wrapped_function_once_per_param(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_file = str(Path(tmp) / "cache.json")
            calls = []

            @cache(cache_file)
            def fn(x: str) -> str:
                calls.append(x)
                return x.upper()

            self.assertEqual(fn("a"), "A")
            self.assertEqual(fn("a"), "A")
            self.assertEqual(calls, ["a"])

    def test_persists_results_to_disk(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_file = str(Path(tmp) / "cache.json")

            @cache(cache_file)
            def fn(x: str) -> str:
                return x.upper()

            fn("hello")

            with open(cache_file) as f:
                self.assertEqual(json.load(f), {"hello": "HELLO"})

    def test_missing_cache_file_starts_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_file = str(Path(tmp) / "does-not-exist.json")

            @cache(cache_file)
            def fn(x: str) -> str:
                return x.upper()

            self.assertEqual(fn("hi"), "HI")


class GetAthleteCountryTests(unittest.TestCase):
    def test_none_returns_none(self) -> None:
        self.assertIsNone(get_athlete_country(None))

    def test_two_letter_code_is_lowercased_passthrough(self) -> None:
        self.assertEqual(get_athlete_country("US"), "us")

    def test_three_letter_code_resolves_to_alpha_2(self) -> None:
        self.assertEqual(get_athlete_country("USA"), "us")

    def test_unknown_three_letter_code_returns_none(self) -> None:
        self.assertIsNone(get_athlete_country("ZZZ"))


class GetCountryCodeTests(unittest.TestCase):
    def test_returns_lowercased_country_code(self) -> None:
        with mock.patch(
            "utils.call_nominatim_api",
            return_value={"address": {"country_code": "VN"}},
        ):
            self.assertEqual(get_country_code("Hanoi"), "vn")

    def test_no_location_returns_none(self) -> None:
        with mock.patch("utils.call_nominatim_api", return_value=None):
            self.assertIsNone(get_country_code("Nowhereville"))

    def test_missing_country_code_key_returns_none(self) -> None:
        with mock.patch("utils.call_nominatim_api", return_value={"address": {}}):
            self.assertIsNone(get_country_code("Somewhere"))


if __name__ == "__main__":
    unittest.main()
