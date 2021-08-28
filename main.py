"""
    Client entrypoint.

"""

import argparse
import time
from pprint import pprint

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


if __name__ == "__main__":
    # Set up command-line args
    parser = argparse.ArgumentParser(description='Python client to WaniKani API.')
    parser.add_argument("api_token", type=str, help="User API token.")
    args = parser.parse_args()


    # Load API token
    HTTP_HEADERS["Authorization"].format(api_token=args.api_token)

    # execute requests
    # NOTE: add throttling to avoid being blocked by API server
    r = requests.get(API_RESETS, headers=HTTP_HEADERS)

    r_json = r.json()
    pprint(r_json)