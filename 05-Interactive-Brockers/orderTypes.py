# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 11:01:37 2026

@author: pabda
"""

#libraries import
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading

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
        
    def nextValidId(self, orderId):
        """
            This method get's the next valid ID to execute a makret's order
        """
        
        #Save it like an attrib
        self.nextOrderId = orderId
    
    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
        """
            This method automatically call's each time who's the order changes on the server
        """
        
        # Shows by console
        print(f"Operation status - OrderId: {orderId}, Status: {status}")
        
    def openOrder(self, orderId, contractt, order, orderState):
        """
            This method returns open orders in our account
        """
        
        # Shows the information
        print(f"OrderId: {orderId}, Order: {order}, Status: {orderState}")
        
        
#Creates the instances
ib = InteractiveBrokers()
#Conectarnos a OB TWS o IB Gateway (By default, TWS uses the 7497 port and the Gateway uses the port 4001)
ib.connect(host="127.0.0.1", port=7497, clientId=1)
api_thread = threading.Thread(target=ib.run)
api_thread.start()

print("Active connection", ib.isConnected())

# Create contract

contract = Contract()
contract.symbol = "MSFT"
contract.secType = "STK"
contract.exchange = "SMART"
contract.currency = "USD"

# Create an Order
order = Order()
order.action = "BUY" # If we want to sell just change to "SELL"
order.totalQuantity = 100
order.Type = "MKT" # That's a market order but if we want a limit we need to change "MKT" to "LMT" and another field
#order.Type = "LMT"
#order.lmtPrice = 428 #<- that 428 means the current price on the stock market
order.eTradeOnly = ""
order.firmQuoteOnly = ""

#Ask for the ID
ib.reqIds(-1) # to get the most recent once
print(ib.nextOrderId)

#Send order to the stock-market
ib.placeOrder(orderId=ib.nextOrderId, contract=contract, order=order)

#Get open orders
ib.reqOpenOrders() # If the order was filled or executed, that code line doesn't happend.

# Reminder:
#   - To execute commands from Python, we must uncheck the "Read-Only API" box.