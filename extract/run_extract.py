from extract.coingecko_client import (
    fetch_with_retry,
    get_current_prices,
    get_timestamp_filename,
    save_json
)

# Run the cryptocurrency data extraction pipeline.

def main():
    coin_ids = ["bitcoin", "ethereum", "solana"]
    data = get_current_prices(coin_ids)
    filepath = get_timestamp_filename("coingecko")
    save_json(data, filepath)
    print(f"Data has been written to {filepath}")


if __name__ == "__main__":
    main()  