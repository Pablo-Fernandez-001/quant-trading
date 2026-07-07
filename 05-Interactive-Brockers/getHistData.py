# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 23:00:42 2026

@author: pabda
"""

# In IB we need a subscription for some data, if you don't have enough, your data going to have a 20 or 30 mins of delay
# Import the libraries
#libraries import
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import pandas as pd

# create class
class InteractiveBrokers(EClient, EWrapper):
    """
        To make easier the API's interaction with InteractiveBrokers
    """
    
    def __init__(self):
        """
            Constructor
        """
        
        #Initialize the EClient class
        EClient.__init__(self,self)
        # creates a dictionary to save the prices
        self.prices = {}
        
        
    def error(self, reqId, errorCode, errorString):
        """
            To manage all errors inside of our application or in our petitions.
        """
        
        # Error
        print(f"Error {reqId} {errorCode}: {errorString}")
    
    def histData(self, reqId, bar):
        """
            That method gets the hist data and saves in a dictionary
        """
        
        data = {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close, "volume": bar.volume}
        
        if reqId not in self.prices:
            self.prices[reqId]=[]
        #Append all data
        self.prices[reqId].append(data)
        
    def historicalDataEnd(self, reqId, start, end):
        """
            This method calls once when we get all the data
        """
        print(f"Downloaded data for ID: {reqId}, into the period {start}.{end}")
        
#Creates the instances
ib = InteractiveBrokers()
#Conectarnos a OB TWS o IB Gateway (By default, TWS uses the 7497 port and the Gateway uses the port 4001)
ib.connect(host="127.0.0.1", port=7497, clientId=1)
api_thread = threading.Thread(target=ib.run)
api_thread.start()

print("Active connection", ib.isConnected())

action_contract = Contract()
action_contract.symbol = "AMZN"
action_contract.secType = "STK"
action_contract.exchange = "SMART"
action_contract.currency = "USD"

# Command execution
final_date = ""
ib.reqMarketDataType(3) # That means we going to get data with delay, if we're suscribed, erase this line
ib.reqHistoricalData(reqId=1, contract=action_contract, endDateTime=final_date, durationStr="5 Y", 
                     barSizeSetting="1 day", whatToShow="TRADES", useRTH=1, formatDate=1, keepUpToDate=False, 
                     chartOptions=[]) ### Documentation for different periods, or more about this function -> https://interactivebrokers.github.io/tws-api/historical_bars.html

# Get data
prices = pd.DataFrame(data=ib.prices[1])
# to fix the datetime format
prices["Date"] = pd.to_datetime(prices["Date"])
prices.set_index("Date",inplace=True)
print(prices)

# Reminder:
#   - Accessing historical data from Interactive Brokers requires appropriate data processing for use and analysis.