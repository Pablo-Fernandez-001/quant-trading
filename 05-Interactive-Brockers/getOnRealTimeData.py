# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 23:29:23 2026

@author: pabda
"""

# We're going to use delay to don't make a payment for use
#libraries import
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import threading
import time

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
        
        
    def error(self, reqId, errorCode, errorString):
        """
            To manage all errors inside of our application or in our petitions.
        """
        
        # Error
        print(f"Error {reqId} {errorCode}: {errorString}")
        
    def piceTick(self, reqId, tickType, price, atrib):
        """
            Method who gets on real time (with a delay)
        """
        # show price and type
        print(f"Tick Price. TickerId: {reqId}, Type: {tickType}, Price: {price}")
        # Tick type, more documentation -> https://interactivebrokers.github.io/tws-api/tick_types.html
        
#Creates the instances
ib = InteractiveBrokers()
#Conectarnos a OB TWS o IB Gateway (By default, TWS uses the 7497 port and the Gateway uses the port 4001)
ib.connect(host="127.0.0.1", port=7497, clientId=1)
api_thread = threading.Thread(target=ib.run)
api_thread.start()

print("Active connection", ib.isConnected())


# Create an action contract
contract = Contract()
contract.symbol = "AMZN"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"


# streaming with datatype
ib.reqMarketDataType(3) # That means we going to get data with delay, if we're suscribed, erase this line
ib.reqMktData(reqId=1, contract=contract, genericTickList="", snapshot=False, regulatorySnapshot=False, mktDataOptions=[])
# on regulatorySnapshot if we uses true, generates a cost 

# wait before to end 
time.sleep(10)

# Cancel the streaming
ib.cancelMktData(reqId=1)

# Disconect ib streaming
ib.disconnect()

# Reminder:
#   - Access to real-time data requires paid subscriptions. However, we can access real-time data
#     that is subject to a time delay (between 10 and 20 minutes).