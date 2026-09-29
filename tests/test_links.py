import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
)

from links import main, search_wikipedia


def _response(status_code: int = 200, payload: dict[str, Any] | None = None) -> mock.Mock:
    resp = mock.Mock()
    resp.status_code = status_code
    resp.json.return_value = payload or {}
    return resp


class SearchWikipediaTests(unittest.TestCase):
    def test_returns_page_url_for_athletic_match(self) -> None:
        payload = {
            "type": "standard",
            "description": "an American marathon runner",
            "extract": "won several championships",
            "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Jane_Doe"}},
        }
        with mock.patch("links.requests.get", return_value=_response(200, payload)):
            self.assertEqual(
                search_wikipedia("Jane Doe"), "https://en.wikipedia.org/wiki/Jane_Doe"
            )

    def test_non_athletic_page_returns_none(self) -> None:
        payload = {
            "type": "standard",
            "description": "a city in Vietnam",
            "extract": "known for its lake",
            "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Hanoi"}},
        }
        with mock.patch("links.requests.get", return_value=_response(200, payload)):
            self.assertIsNone(search_wikipedia("Hanoi"))

    def test_non_200_response_returns_none(self) -> None:
        with mock.patch("links.requests.get", return_value=_response(404, {})):
            self.assertIsNone(search_wikipedia("Nobody"))

    def test_request_exception_returns_none(self) -> None:
        with mock.patch("links.requests.get", side_effect=RuntimeError("network down")):
            self.assertIsNone(search_wikipedia("Jane Doe"))


class MainTests(unittest.TestCase):
    def test_writes_links_for_new_athletes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "athletes.json"
            output_path = Path(tmp) / "links.json"
            input_path.write_text(json.dumps([{"Name": "Jane Doe"}, {"Name": "John Roe"}]))

            with mock.patch(
                "links.search_wikipedia",
                side_effect=lambda name: f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}",
            ):
                main([str(input_path)], str(output_path))

            result = json.loads(output_path.read_text())
            self.assertEqual(
                result,
                {
                    "Jane Doe": "https://en.wikipedia.org/wiki/Jane_Doe",
                    "John Roe": "https://en.wikipedia.org/wiki/John_Roe",
                },
            )

    def test_skips_athletes_already_in_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "athletes.json"
            output_path = Path(tmp) / "links.json"
            input_path.write_text(json.dumps([{"Name": "Jane Doe"}]))
            output_path.write_text(json.dumps({"Jane Doe": "https://existing"}))

            with mock.patch("links.search_wikipedia") as search:
                main([str(input_path)], str(output_path))
                search.assert_not_called()

            self.assertEqual(json.loads(output_path.read_text()), {"Jane Doe": "https://existing"})

    def test_missing_input_file_is_skipped_without_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "links.json"
            main([str(Path(tmp) / "missing.json")], str(output_path))
            self.assertEqual(json.loads(output_path.read_text()), {})


if __name__ == "__main__":
    unittest.main()
