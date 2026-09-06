# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 23:30:42 2026

@author: pabda
"""

# Import libraries
import fxcmpy
import time
 
# API Token
api_token = "API_TOKEN"
 
# Create an instance of the FXCM API connection
connection = fxcmpy.fxcmpy(access_token=api_token, log_level="error")
 
# Verify that we are connected
if connection.is_connected():
    # Define the instrument and order parameters
    instrument = "EUR/USD"
    amount = 10  # Position size (in lots)
    is_buy = True  # True for buy, False for sell
    order_type = "AtMarket"  # Order type
 
    # Send buy order
    order = connection.open_trade(symbol=instrument, is_buy=is_buy, amount=amount, time_in_force="GTC", order_type=order_type)
    print(f"Order sent for {instrument}:")
    
    # Wait for execution
    time.sleep(1)
 
    # Show order details
    print(order)
 
    # Get open positions
    open_positions = connection.get_open_positions()
    print("\nOpen positions:")
    print(open_positions)
 
    # Close the position after some time
    time.sleep(10)  # Wait 10 seconds before closing the position
 
    # Check if there are open positions
    if not open_positions.empty:
        position_id = open_positions.iloc[0]["tradeId"]  # Get the position ID
        connection.close_trade(trade_id=position_id, amount=amount)
        print(f"\nPosition {position_id} closed.")
    
    # Get open positions after closing
    open_positions = connection.get_open_positions()
    print("\nOpen positions after closing:")
    print(open_positions)
 
else:
    print("Error connecting to the API")
 
# Disconnect from the API
connection.close()
 
#- Reminder: 
#   - Order creation and execution management must be handled very carefully. 