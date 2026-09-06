# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 23:29:38 2026

@author: pabda
"""

 # Import libraries
import fxcmpy
import time
 
# FXCM API Token
api_token = "API_TOKEN"
 
# Create an instance of the FXCM API connection
connection = fxcmpy.fxcmpy(access_token=api_token, log_level="error")
 
# Callback to process streaming data
def print_data(data, dataframe):
    print("Received data:")
    # Print the last row of data
    print(dataframe.tail(1)) 
 
# Verify that we are connected
if connection.is_connected():
    # Instrument to subscribe to
    instrument = "EUR/USD"
 
    # Subscribe to the instrument (this will start receiving data)
    connection.subscribe_market_data(instrument, (print_data,))
    print(f"Subscribed to {instrument} data.")
 
    # Start time
    start_time = time.time()
    duration = 30  # Duration in seconds
 
    # Keep the script running and receive data for the specified time
    while time.time() - start_time < duration:
        time.sleep(1)  # Wait 1 second between iterations
 
    # Unsubscribe and close the connection after 30 seconds
    connection.unsubscribe_market_data(instrument)
    connection.close()
    print("Disconnected and subscription canceled after 30 seconds.")
    
else:
    print("Error connecting to the API")
 
#- Reminder:
#   - Real-time data must be processed correctly in order to use it effectively.
