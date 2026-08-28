from pathlib import Path
import duckdb

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
WAREHOUSE_DIR = PROJECT_ROOT / "data" / "warehouse"
DB_PATH = WAREHOUSE_DIR / "crypto.duckdb"

def load_json_to_duckdb():
# Creat folder warehouse if it doesn't exit
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)


# Find all JSON file in data/raw
json_files = list(RAW_DATA_DIR.glob("*.json"))

if not json_files:
    raise FileNotFoundError(
        f"Không tìm thấy file JSON nào trong: {RAW_DATA_DIR}"
    )

print(f"Found {len(json_files)} JSON file(s):")

for json_file in json_files:
    print(f"  - {json_file.name}")

# Connect to DuckDB
con = duckdb.connect(str(DB_PATH))

try:
    # Read all JSON file
    con.execute(
        """
        CREATE OR REPLACE TABLE raw_crypto_prices AS
        SELECT *
        FROM read_json_auto(
            ?,
            format='array',
            union_by_name=true
        )
        """,
        [[str(file) for file in json_files]]
    )

    # Check the result
    row_count = con.execute(
        """
        SELECT COUNT(*)
        FROM raw_crypto_prices
        """
    ).fetchone()[0]

    print("\nSuccessfully loaded data into DuckDB")
    print(f"Database: {DB_PATH}")
    print("Table: raw_crypto_prices")
    print(f"Total rows: {row_count}")

    # Show common data
    results = con.execute(
        """
        SELECT
            id,
            symbol,
            name,
            current_price,
            market_cap,
            last_updated
        FROM raw_crypto_prices
        ORDER BY last_updated DESC
        """
    ).fetchall()

    print("\nLoaded data:")

    for row in results:
        print(row)

finally:
    con.close()


if __name__ == "__main__":
    load_json_to_duckdb()
