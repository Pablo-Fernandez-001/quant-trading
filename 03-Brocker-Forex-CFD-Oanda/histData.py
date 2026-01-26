# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 15:01:48 2026

@author: pabda
"""

import tpqoa

# Generate connection
oanda = tpqoa.tpqoa(conf_file="config.cfg")

#params
ticker = "XAU_USD"
init = "2023-01-01"
end = "2024-01-01"

#hist data
help(oanda.get_history)

# daily data
'''

Category 	Codes	                      Examples
Seconds	  S5, S10, S15, S30	              5, 10, 15, or 30-second candlesticks
Minutes	  M1, M2, M4, M5, M10, M15, M30	  1, 2, 4, 5, 10, 15, or 30-minute candlesticks
Hours	  H1, H2, H3, H4, H6, H8, H12	  1, 2, 3, 4, 6, 8, or 12-hour candlesticks
Day	D	  Daily                           candlesticks
Week	  W	                              Weekly candlesticks
Month  	  M	                              Monthly candlesticks

price (string): Specifies the price type:
'A' for ask prices -> Buy, price who's the market sells to me
'B' for bid prices -> Sell, price who's the market buy to me
'M' for midpoint prices (average of bid and ask). -> Average = (A+B)/2

'''
df = oanda.get_history(instrument=ticker, start=init, end=end, granularity="D", price="M")


# showing data
print(f"Rows: {df.shape[0]}")
print(df)


# intra day data
# Use January 3rd instead of January 1st (markets are usually closed on New Year's Day)
df = oanda.get_history(instrument=ticker, start="2023-01-03", end="2023-01-04", granularity="S5", price="M")

# showing data
print(f"Rows: {df.shape[0]}")
print(df)

# hour data
df = oanda.get_history(instrument=ticker, start="2023-01-03", end="2023-01-04", granularity="H1", price="M")
 
# showing data
print(f"Rows: {df.shape[0]}")
print(df)

# get current prices
print(oanda.get_prices(instrument=ticker))


# Reminder:
# - The tpqoa library removes OANDA’s limitations by automatically handling large
# data volumes without manual intervention.