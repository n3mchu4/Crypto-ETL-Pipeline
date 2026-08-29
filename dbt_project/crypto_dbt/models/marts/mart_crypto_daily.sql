{{ config(materialized='table') }}

SELECT
    CAST(last_updated AS DATE) AS trade_date,
    id,
    symbol,
    name,

    AVG(current_price) AS avg_price,
    MAX(current_price) AS max_price,
    MIN(current_price) AS min_price,

    AVG(market_cap) AS avg_market_cap,
    AVG(total_volume) AS avg_total_volume,

    AVG(price_change_percentage_24h) AS avg_price_change_percentage_24h

FROM {{ ref('stg_crypto_prices') }}

GROUP BY
    CAST(last_updated AS DATE),
    id,
    symbol,
    name