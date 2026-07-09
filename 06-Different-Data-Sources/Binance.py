# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 23:54:41 2026

@author: pabda
"""

# Binance's API Documentation -> https://binance-docs.github.io/apidocs/spot/en/#change-log
# Import libs
import pandas as pd
import requests
import time
import matplotlib.pyplot as plt


# Define base url
base_url = "https://api.binance.com"
endpoint_conn = "/api/v3/ping"
endpoint_inst = "/api/v3/exchangeInfo"
endpoint_data = "/api/v3/klines"


# Test connectivity
r = requests.get(url=base_url + endpoint_conn)
content = r.json()

if content == {}:
    print("Binance API's connectivity was successful")


# Get symbol list
r = requests.get(url=base_url + endpoint_inst)
content = r.json()

instrument_list = []

for instrument in content["symbols"]:
    instrument_list.append(instrument["symbol"])

print(len(instrument_list))
print(instrument_list[:10])


# Get historical data
def get_data(ticker, start_date, end_date, interval) -> pd.DataFrame:
    """
    Obtains historical OHLCV data from Binance API.
    Supports pagination because Binance only returns up to 1000 candles per request.
    """

    start_time = int(pd.to_datetime(start_date).timestamp() * 1000)
    end_time = int(pd.to_datetime(end_date).timestamp() * 1000)

    all_prices = []

    while start_time < end_time:

        params = {
            "symbol": ticker,
            "interval": interval,
            "startTime": start_time,
            "endTime": end_time,
            "limit": 1000
        }

        r = requests.get(url=base_url + endpoint_data, params=params)
        content = r.json()

        # Validate Binance error response
        if isinstance(content, dict):
            raise Exception(f"Binance API error -> {content}")

        # If Binance returns no more data, stop
        if len(content) == 0:
            break

        for data in content:
            date = pd.to_datetime(data[0], unit="ms")
            open_price = float(data[1])
            high_price = float(data[2])
            low_price = float(data[3])
            close_price = float(data[4])
            volume = float(data[5])

            all_prices.append([
                date,
                open_price,
                high_price,
                low_price,
                close_price,
                volume
            ])

        # Move start_time to the next candle after the last received candle
        last_open_time = content[-1][0]
        start_time = last_open_time + 1

        # Small pause to avoid hitting rate limits too aggressively
        time.sleep(0.1)

    df = pd.DataFrame(
        data=all_prices,
        columns=["Date", "Open", "High", "Low", "Close", "Volume"]
    )

    if not df.empty:
        df.set_index("Date", inplace=True)

    return df


# Data download 1s - We can use that kind of information in HFT (High Frequency Trading)
df = get_data(
    ticker="BTCUSDT",
    start_date="2024-01-01 00:00:00",
    end_date="2024-01-01 00:05:00",
    interval="1s"
)

print(df)

# Data download 1 min - We can use that kind of information in HFT (High Frequency Trading)
df = get_data(
    ticker="BTCUSDT",
    start_date="2024-01-01 00:00:00",
    end_date="2024-01-01 00:05:00",
    interval="1m"
)

print(df)

# Data download 15 min - We can use that kind of information in HFT (High Frequency Trading)
df = get_data(
    ticker="BTCUSDT",
    start_date="2024-01-01 00:00:00",
    end_date="2024-01-01 00:05:00",
    interval="15m"
)

print(df)

# Data download 1 hour - We can use that kind of information in HFT (High Frequency Trading)
df = get_data(
    ticker="BTCUSDT",
    start_date="2024-01-01 00:00:00",
    end_date="2024-01-01 00:05:00",
    interval="1h"
)

print(df)

# Data download 6 hours - We can use that kind of information in HFT (High Frequency Trading)
df = get_data(
    ticker="BTCUSDT",
    start_date="2024-01-01 00:00:00",
    end_date="2024-01-01 00:05:00",
    interval="6h"
)

print(df)

# Data download 12 hours - We can use that kind of information in HFT (High Frequency Trading)
df = get_data(
    ticker="BTCUSDT",
    start_date="2024-01-01 00:00:00",
    end_date="2024-01-01 00:05:00",
    interval="12h"
)

print(df)

# Data download 1 Day - We can use that kind of information in HFT (High Frequency Trading)
df = get_data(
    ticker="BTCUSDT",
    start_date="2024-01-01 00:00:00",
    end_date="2024-01-01 00:05:00",
    interval="1d"
)

print(df)


# Data download 1 Month - We can use that kind of information in HFT (High Frequency Trading)
df = get_data(
    ticker="BTCUSDT",
    start_date="2024-01-01 00:00:00",
    end_date="2024-01-01 00:05:00",
    interval="1M"
)

print(df)

# Reminder:
#   - The Binance API allows you to retrieve data at various time intervals, which is useful for different
#     types of analysis and trading strategies.