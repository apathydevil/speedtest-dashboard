import os

import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SPEEDTEST_URL")
token = os.getenv("SPEEDTEST_TOKEN")

headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}


def get_latest_result() -> None | dict:
    try:
        response = requests.get(f"{url}/api/v1/results/latest", headers=headers)
        data = response.json()
        latest = data["data"]
        if latest["status"] != "completed":
            return {"status": latest["status"]}
        return {
            "status": latest["status"],
            "download": latest["download_bits_human"],
            "upload": latest["upload_bits_human"],
            "ping": latest["ping"],
            "created_at": latest["created_at"],
            "download_elapsed": latest["data"]["download"]["elapsed"] / 1000,
            "upload_elapsed": latest["data"]["upload"]["elapsed"] / 1000,
        }
    except requests.RequestException as e:
        print(e)


def get_stats() -> None | dict:
    try:
        response = requests.get(f"{url}/api/v1/stats", headers=headers)
        return response.json()["data"]
    except requests.RequestException as e:
        print(e)


def get_result_history() -> None | dict:
    try:
        response = requests.get(
            f"{url}/api/v1/results",
            headers=headers,
            params={"page[size]": 10, "sort": "-created_at"},
        )
        return response.json()["data"]
    except requests.RequestException as e:
        print(e)


def run_speedtest() -> None | str:
    try:
        response = requests.post(f"{url}/api/v1/speedtests/run", headers=headers)
        return response.json()["message"]
    except requests.RequestException as e:
        print(e)
