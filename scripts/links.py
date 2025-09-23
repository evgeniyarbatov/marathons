#!/usr/bin/env python3
"""
Script to fetch Wikipedia page links for marathon athletes.
Usage: python3 fetch_wikipedia_links.py <input_csv> <output_json>
"""

import sys
import csv
import json
import requests
import time
import os
from urllib.parse import quote

import requests
from urllib.parse import quote
import time

def search_wikipedia(athlete_name):
    base_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"

    try:
        # URL encode the query
        encoded_query = quote(athlete_name.replace(" ", "_"))
        url = f"{base_url}{encoded_query}"

        headers = {
            "User-Agent": "MarathonRunners"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data.get('type') == 'standard':
                description = data.get('description', '').lower()
                extract = data.get('extract', '').lower()

                athletic_keywords = [
                    'runner', 'athlete', 'marathon',
                    'distance', 'olympic', 'championship'
                ]

                if any(keyword in description or keyword in extract for keyword in athletic_keywords):
                    return data.get('content_urls', {}).get('desktop', {}).get('page')

        time.sleep(0.1)

    except Exception as e:
        print(f"Error searching for {athlete_name}: {e}")

    return None

def main(csv_file, output_file):
    """Main function to process marathon data and fetch Wikipedia links."""

    # Check if input file exists
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found")
        return

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Load existing links if file exists
    wikipedia_links = {}
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as file:
                wikipedia_links = json.load(file)
            print(f"Loaded {len(wikipedia_links)} existing Wikipedia links")
        except Exception as e:
            print(f"Error loading existing file: {e}")

    processed_athletes = set()

    print("Reading marathon data...")

    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row.get('Name', '').strip()
                country = row.get('Country', '').strip()

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
                        with open(output_file, 'w', encoding='utf-8') as file:
                            json.dump(wikipedia_links, file, indent=2, ensure_ascii=False)
                    except Exception as e:
                        print(f"Error saving after finding link: {e}")
                else:
                    print(f"  ✗ Not found")

                # Be respectful to Wikipedia's servers
                time.sleep(0.2)

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Final save
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(wikipedia_links, file, indent=2, ensure_ascii=False)

        print(f"\nWikipedia links saved to: {output_file}")
        print(f"Found links for {len(wikipedia_links)} out of {len(processed_athletes)} unique athletes")

        # Print summary
        found_count = len(wikipedia_links)
        total_count = len(processed_athletes)
        print(f"Success rate: {found_count}/{total_count} ({found_count/total_count*100:.1f}%)")

    except Exception as e:
        print(f"Error saving results: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])