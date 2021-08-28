"""
    Client entrypoint.

"""

import argparse
import logging
import time
from pprint import pprint

import pandas as pd
import requests


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
    parser.add_argument("--level", type=int, default=0, help="WaniKani level.")
    parser.add_argument(
        "--items",
        type=str,
        default="",
        help="Comma-separated (no spaces!) list of WaniKani item types (kanji, vocabulary, radical)."
    )
    args = parser.parse_args()

    # Load API token into headers
    HTTP_HEADERS["Authorization"] = HTTP_HEADERS["Authorization"].format(api_token=args.api_token)

    # Assemble query
    url = API_SUBJECTS
    if args.level or args.items:
        url += "?"

    if args.items:
        url += f"types={args.items}"
    
    if "types" in url:
        url += "&"

    if args.level > 0:
        url += f"level={args.level}"

    # Execute requests
    # NOTE: add throttling to avoid being blocked by API server?
    r = requests.get(url, headers=HTTP_HEADERS)
    r_json = r.json()

    if "data" not in r_json:
        logging.critical(f"Failed to get items for URL: {url}")
        logging.critical(r.text)
        exit(1)

    data: list = r_json["data"]
    pprint(data[:2])

    # TODO: Filter out/flatten "data" field of each item to extract useful info
    filtered_data = []
    for el in data[:20]:     # type: dict
        filtered_data.append(
            {
                "WK Level": el["data"]["level"],
                "Spelling": el["data"]["characters"],       # kanji
                **{f"Reading {i}": reading["reading"] for i, reading in enumerate(el["data"]["readings"])},
                **{f"Meaning {i}": meaning["meaning"] for i, meaning in enumerate(el["data"]["meanings"])}
            }
        )

    pprint(filtered_data)

    # Convert to pandas.DataFrame
    df = pd.DataFrame(filtered_data)
    print(df)

    # Filter content
    # print(df[df["object"] == "kanji"])
    # print(df)
