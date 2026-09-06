# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 23:27:04 2026

@author: pabda
"""

# Import libraries
import fxcmpy
 
# API Token
api_token = "API_TOKEN"
 
# Create an instance of the FXCM API connection
connection = fxcmpy.fxcmpy(access_token=api_token, log_level="error")
 
# Verify that we are connected
if connection.is_connected():
    # Get account details
    account_details = connection.get_accounts()
    print("Account details:")
    print(account_details)
 
    # Get account summary
    account_info = connection.get_account_summary()
    print("\nAccount summary:")
    print(account_info)
 
    # Get the list of available instruments
    instruments = connection.get_instruments()
    print("\nList of instruments:")
    print(instruments)
else:
    print("Error connecting to the API")
 
# Disconnect from the API
connection.close()
 
#- Reminder:
#   - The FXCM API also uses an authentication token that allows account access from Python.
