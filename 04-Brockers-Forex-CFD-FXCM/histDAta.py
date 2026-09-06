# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 23:28:53 2026

@author: pabda
"""

# Import libraries
import fxcmpy
 
# API token obtained from FXCM
api_token = "API_TOKEN"
 
# Create an instance of the FXCM API connection
connection = fxcmpy.fxcmpy(access_token=api_token, log_level="error")
 
# Verify that we are connected
if connection.is_connected():
    
    # Get historical market data for EUR/USD
    instrument = "EUR/USD"
    period = "D1"  # Candle period (D1 = daily)
    number_of_candles = 100  # Number of candles to retrieve
 
    # Get a specific number of candles
    data = connection.get_candles(instrument, period=period, number=number_of_candles)
    print(f"Most recent data for {instrument}:")
    print(data)
    
    # Get data between dates
    start_date = "2023-01-01"
    end_date = "2024-01-01"
    prices = connection.get_candles(instrument, start=start_date, end=end_date, period=period)
    print(f"Historical data for {instrument}:")
    print(prices)
    
    # Available Time Frames
    # "m1", "m5", "m15", "m30", "H1", "H2", "H3", "H4", "H6", "H8", "D1", "W1", "M1"
    
    # Get Most Recent Price
    current_price = connection.get_last_price(instrument)
    print(f"The most recent price for {instrument} is:")
    print(current_price)
    
else:
    print("Error connecting to the API")
 
# Disconnect from the API
connection.close()
 
#- Reminder:
#   - There is a limit of 10,000 rows of information per query.