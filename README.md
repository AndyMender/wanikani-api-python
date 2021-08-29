# wanikani-api-python
A simple Python API wrapper for WaniKani in Python

Official WaniKani API documentation: https://docs.api.wanikani.com/20170710/#introduction

# **WARNING:** The main `subjects` endpoint for items returns only up to 1000 items at a time so filtering per level is recommended

# HowTo:
1. Install Python requirements:
```shell
python3 -m pip install --user -r requirements.txt
```
2a. Run main script:
```shell
python3 main.py <your_api_token>
```
2b. Run main script with level and item type selection:
```shell
for i in {1..10}
do
    python3 main.py "$BEARER_TOKEN" --levels "$i" --items "vocabulary"
done
```
