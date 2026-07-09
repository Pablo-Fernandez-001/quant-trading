# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 00:11:05 2026

@author: pabda
"""
# Documentation -> https://github.com/ranaroussi/yfinance

# -*- coding: utf-8 -*-
# Import libraries
import yfinance as yf  # pip install yfinance

# Define parameters
ticker = "AAPL"
start_date = "2021-01-01"
end_date = "2024-01-01"

# Daily data
df = yf.download(tickers=ticker, start=start_date, end=end_date, interval="1d")
print(df)

# One-minute data
df = yf.download(tickers=ticker, interval="1m")
print(df)

# One-hour data - does not be more than 2 years in an hour
df = yf.download(tickers=ticker, start="2023-01-01", interval="1h")
print(df)

# Weekly data
df = yf.download(tickers=ticker, start=start_date, end=end_date, interval="1wk")
print(df)

# Monthly data
df = yf.download(tickers=ticker, start=start_date, end=end_date, interval="1mo")
print(df)

# Cryptocurrencies
df = yf.download(tickers="BTC-USD", start=start_date, end=end_date, interval="1d")
print(df)

# Create a Yahoo Finance Ticker object
stock = yf.Ticker(ticker="MSFT")
stock_info = stock.info

# Print relevant information
print("Symbol:", stock_info["symbol"])
print("Name:", stock_info["longName"])
print("Current Price:", stock_info["currentPrice"])
print("Currency:", stock_info["currency"])
print("Website:", stock_info["website"])

# Get the company summary
print("\nCompany Summary:")
for key, value in stock_info.items():
    print(f"{key}: {value}")

# Get the balance sheet
balance_sheet = stock.balance_sheet
print("\nBalance Sheet:")
print(balance_sheet)

# Get the income statement
income_statement = stock.financials
print("\nIncome Statement:")
print(income_statement)

# Dividends
dividends = stock.dividends
print("\nDividends:")
print(dividends)

# Get the cash flow statement
cashflow = stock.cashflow
print("\nCash Flow Statement:")
print(cashflow)

# Reminder:
#   - yfinance is a very broad library that allows us to extract information
#     across different timeframes, and it also provides a wide range of useful
#     financial information for a more complete analysis of different assets.