import requests
import time
import os
import json
from datetime import datetime

# Send a GET request with retry logic to handle temporary API failure and rate limiting.
def fetch_with_retry(url, params, max_retries=3, wait_seconds=5):  #
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                time.sleep(wait_seconds)
            else:
                time.sleep(wait_seconds)
        except requests.exceptions.RequestException:
            time.sleep(wait_seconds)
    raise Exception("Failed to fetch data after multiple attempts")

# Fetch current cryptocurrency market data from CoinGecko.
def get_current_prices(coin_ids: list[str]) -> dict:   
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "ids": ",".join(coin_ids)}
    return fetch_with_retry(url, params)

# Generate a date-based file path for storing raw API data.
def get_timestamp_filename(prefix: str) -> str:   
    timestamp = datetime.now().strftime("%Y-%m-%d")
    return f"data/raw/{prefix}_{timestamp}.json"

# Create the target directory if needed and save data as JSON.
def save_json(data, filepath):   
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
        
def main():
    coin_ids = ["bitcoin", "ethereum", "solana"]

    data = get_current_prices(coin_ids)

    filepath = get_timestamp_filename("coingecko")

    save_json(data, filepath)

    print(f"Data has been written to {filepath}")



if __name__ == "__main__":
    main()
