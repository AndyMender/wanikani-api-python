"""
    Client entrypoint.

"""

import argparse
import logging
import os
import time
from pprint import pprint

import pandas as pd
import requests

# Local storage definitions
DATA_DIR = "wk_items"
CSV_SLUG = "{levels}_{items}.csv"

# Request headers
HTTP_HEADERS = {
    "Wanikani-Revision": "20170710",            # can change?
    "Authorization": "Bearer {api_token}",      # User API token is loaded here
    "content-type": "application/json"          # optional
}

# Endpoints
API_MAIN = "https://api.wanikani.com/v2/"
API_RESETS = API_MAIN + "resets"
API_REVIEWS = API_MAIN + "reviews"
API_STUDY_MATERIALS = API_MAIN + "study_materials"
API_SUBJECTS = API_MAIN + "subjects"


if __name__ == "__main__":
    # Set up command-line args
    parser = argparse.ArgumentParser(description='Python client to WaniKani API.')
    parser.add_argument("api_token", type=str, help="User API token.")
    parser.add_argument("--levels", type=str, default="", help="Comma-separated (no spaces!) list of WaniKani levels.")
    parser.add_argument(
        "--items",
        type=str,
        default="",
        help="Comma-separated (no spaces!) list of WaniKani item types (kanji, vocabulary, radical)."
    )
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG)

    # Set up local storage
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath: str = os.path.join(
        DATA_DIR,
        CSV_SLUG.format(
            levels=args.levels if args.levels else "all",
            items=args.items if args.items else "all"
        )
    )
    if os.path.isfile(filepath):
        logging.warning(f"CSV datafile already exists. Will overwrite: {filepath}")

    # Load API token into headers
    HTTP_HEADERS["Authorization"] = HTTP_HEADERS["Authorization"].format(api_token=args.api_token)

    # Assemble query
    url = API_SUBJECTS
    if args.levels or args.items:
        url += "?"

    if args.items:
        url += f"types={args.items}"
    
    if "types" in url and args.levels:
        url += "&"

    if args.levels:
        url += f"levels={args.level}"

    logging.info(f"Full WaniKani URL: {url}")

    # Execute requests
    # NOTE: add throttling to avoid being blocked by API server?
    r = requests.get(url, headers=HTTP_HEADERS)
    r_json: dict = r.json()

    # Extract main "data" field from JSON response
    if "data" not in r_json:
        logging.critical(f"Failed to get items for URL: {url}")
        logging.critical(r.text)
        exit(1)
    data: list = r_json["data"]
    # pprint(data[:2])

    # Transform data to expected format
    filtered_data = []
    for el in data:     # type: dict
        filtered_data.append(
            {
                "WK Level": el["data"]["level"],
                "Spelling": el["data"]["characters"],               # kanji
                "Reading": el["data"]["readings"][0]["reading"],    # kana (one of the readings)
                "Meaning": el["data"]["meanings"][0]["meaning"]     # one of the meanings
                # TODO: Multiple meanings needed at all...?
                # **{f"Reading {i}": reading["reading"] for i, reading in enumerate(el["data"]["readings"])},
                # **{f"Meaning {i}": meaning["meaning"] for i, meaning in enumerate(el["data"]["meanings"])}
            }
        )

    pprint(filtered_data[:5])

    # Convert to pandas.DataFrame
    df = pd.DataFrame(filtered_data)
    print(df.head(20))

    # Dump to file
    df.to_csv(filepath, sep=",")
