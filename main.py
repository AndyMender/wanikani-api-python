"""
    Client entrypoint.

"""

import argparse
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
    args = parser.parse_args()


    # Load API token
    HTTP_HEADERS["Authorization"] = HTTP_HEADERS["Authorization"].format(api_token=args.api_token)

    # execute requests
    # NOTE: add throttling to avoid being blocked by API server
    r = requests.get(API_SUBJECTS, headers=HTTP_HEADERS)

    r_json = r.json()
    # pprint(r_json["data"])
    if "data" in r_json:
        df = pd.DataFrame(r_json["data"])
    else:
        print("Failed API call. Aborting!")
        exit(1)
    print(df)
