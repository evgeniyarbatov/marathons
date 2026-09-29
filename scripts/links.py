#!/usr/bin/env python3
"""
Script to fetch Wikipedia page links for marathon athletes.
Usage: python3 links.py <input_json1> <input_json2> ... <output_json>
"""

import json
import os
import sys
import time
from urllib.parse import quote

import requests


def search_wikipedia(athlete_name: str) -> str | None:
    base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"

    try:
        # URL encode the query
        encoded_query = quote(athlete_name.replace(" ", "_"))
        url = f"{base_url}{encoded_query}"

        headers = {"User-Agent": "MarathonRunners"}

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data.get("type") == "standard":
                description = data.get("description", "").lower()
                extract = data.get("extract", "").lower()

                athletic_keywords = [
                    "runner",
                    "athlete",
                    "marathon",
                    "distance",
                    "olympic",
                    "championship",
                ]

                if any(
                    keyword in description or keyword in extract for keyword in athletic_keywords
                ):
                    page: str | None = data.get("content_urls", {}).get("desktop", {}).get("page")
                    return page

        time.sleep(0.1)

    except Exception as e:
        print(f"Error searching for {athlete_name}: {e}")

    return None


def main(input_files: list[str], output_file: str) -> None:
    """Main function to process marathon JSON data and fetch Wikipedia links."""

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Load existing links if file exists
    wikipedia_links = {}
    if os.path.exists(output_file):
        try:
            with open(output_file, encoding="utf-8") as file:
                wikipedia_links = json.load(file)
            print(f"Loaded {len(wikipedia_links)} existing Wikipedia links")
        except Exception as e:
            print(f"Error loading existing file: {e}")

    processed_athletes = set()

    print("Reading marathon data from JSON files...")

    # Process each input JSON file
    for json_file in input_files:
        print(f"Processing {json_file}...")

        # Check if input file exists
        if not os.path.exists(json_file):
            print(f"Warning: {json_file} not found, skipping")
            continue

        try:
            with open(json_file, encoding="utf-8") as file:
                data = json.load(file)

            for entry in data:
                name = entry.get("Name", "").strip()

                if not name or name in processed_athletes:
                    continue

                processed_athletes.add(name)

                # Skip if we already have a link for this athlete
                if name in wikipedia_links:
                    print(f"Skipping {name} (already have link)")
                    continue

                print(f"Searching Wikipedia for: {name}")

                wikipedia_url = search_wikipedia(name)

                if wikipedia_url:
                    wikipedia_links[name] = wikipedia_url
                    print(f"  ✓ Found: {wikipedia_url}")

                    # Save immediately after finding a link
                    try:
                        with open(output_file, "w", encoding="utf-8") as file:
                            json.dump(wikipedia_links, file, indent=2, ensure_ascii=False)
                            file.write("\n")
                    except Exception as e:
                        print(f"Error saving after finding link: {e}")
                else:
                    print("  ✗ Not found")

                # Be respectful to Wikipedia's servers
                time.sleep(0.2)

        except Exception as e:
            print(f"Error reading JSON file {json_file}: {e}")
            continue

    # Final save
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(wikipedia_links, file, indent=2, ensure_ascii=False)
            file.write("\n")

        print(f"\nWikipedia links saved to: {output_file}")
        print(
            f"Found links for {len(wikipedia_links)} out of {len(processed_athletes)} unique athletes"
        )

        # Print summary
        found_count = len(wikipedia_links)
        total_count = len(processed_athletes)
        if total_count > 0:
            print(
                f"Success rate: {found_count}/{total_count} ({found_count / total_count * 100:.1f}%)"
            )

    except Exception as e:
        print(f"Error saving results: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 links.py <input_json1> [input_json2] ... <output_json>")
        sys.exit(1)

    # All arguments except the last one are input files
    input_files = sys.argv[1:-1]
    output_file = sys.argv[-1]

    main(input_files, output_file)
