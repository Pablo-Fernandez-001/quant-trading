# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 23:28:25 2026

@author: pabda
"""

#import libs
import yfinance as yf


#defining ticker and getting data
ticker = "AAPL"
asset = yf.Ticker(ticker)
cash_flow = asset.cash_flow


#Defining params for the valuate's model
growth_rate = 0.03 # Annualizated grow rate estimated to a free cash flow
discount_rate = 0.1 # Discount rate to discount te present value in each flow
terminal_growth_rate = 0.02 # Perpetual Grow rate before the projection period
projection_years = 5 # Years number to proyect the cash flow

# Get the free cash flow (FCF) from the rescently year
fcf = cash_flow.loc["Free Cash Flow"][0]

# Project FCF to the next years
fcf_projections = [fcf * (1 + growth_rate) ** i for i in range(1, projection_years + 1)]

# Calculates Terminal Values
terminal_value = fcf_projections[-1] * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)

# Discount the cash flows and the present terminal value
dcf_value = sum([fcf / (1 + discount_rate) ** (i + 1) for i, fcf in enumerate(fcf_projections)])
dcf_value += terminal_value / (1 + discount_rate) ** projection_years

# Get the number of outstanding assets 
outstanding_assets = asset.info["sharesOutstanding"]

# Calculates the intrinsecal value of the asset
intrinsecal_value_by_asset = dcf_value / outstanding_assets
print(f"Intrinsic Value of {ticker}: ${intrinsecal_value_by_asset:.2f} per share")
print(f"Current Value of {ticker}: ${asset.info['currentPrice']}")

# Reminder:
#   - The Growth Rate represents an estimate of the annual free cash flow growth. 3% is a
#     conservative and reasonable assumption for many mature companies.
#   - The Discount Rate is used to discount future cash flows to present value. 10% is a
#     commonly used rate that reflects a company's cost of capital.
#   - The Terminal Growth Rate represents the perpetual growth of cash flow beyond the projection period.
#     2% is a conservative assumption reflecting the long-term growth of the economy.
#   - A 5-year period for projecting cash flows is standard and allows for a reasonable projection
#     without being overly uncertain.
#   - Intrinsic value is the true valuation of a company based on financial fundamentals, independent of its market
#     price.