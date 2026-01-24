# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 22:09:57 2026

@author: pabda
"""

import tpqoa
import json
import configparser
import os

# Create Credential Document
config = configparser.ConfigParser()

#add section and option with values
config["oanda"]={
        "account_id":"101-001-38314985-001",
        "access_token":"460f7a4a26ad081f5ac8c4bad7349e8b-afccf3b70cc332f690caf13be449766b",
        "account_type":"practice"
    }

#Create configuration file
file = "config.cfg"
if not os.path.isfile(file):
    with open(file, "w") as configfile:
        config.write(configfile)
        
        
# connection
oanda = tpqoa.tpqoa(conf_file=file)

print(f"Account number {oanda.account_id}")
print(f"Access token: {oanda.access_token}")
print(f"Account type: {oanda.access_token}")
print(f"Hostname: {oanda.hostname}")


# get account information
account_info = oanda.get_account_summary()
print(json.dumps(account_info, indent=4))

# available instruments
instruments = oanda.get_instruments()

for name, ticker in instruments:
    print(f"Instrument Name: {name}, ticker: {ticker}")
    
print(f"Total number of instruments: {len(instruments)}")

#Reminder:
# - The tpqoa library is a wrapper for the official OANDA library (v20) that facilitates access to the OANDA REST API.