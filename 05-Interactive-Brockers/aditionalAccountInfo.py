# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 13:29:28 2026

@author: pabda
"""

#To close if the order it's going bad
from ibapi.client import EClient # Comunication to Interactive Brokers (IB)
from ibapi.wrapper import EWrapper # That one gets the servers answer and process them
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
    
    def accountSummary(self, reqId, account, tag, value, currency):
        
        """
            Gets the account information
        """
        
        #print the information
        print(f"Account summary - Account: {account}, Tag: {tag}, Value: {value}, currency: {currency}")

    def pnl(self, reqId, dailyPnL, unrealizedPnL, realizedPnL):
        """
            This method returns Profit or loss to the account
        """
        
        #Show by console
        # Mostrar por consola
        print(f"ReqId:{reqId}, \n Daily Profit/Lost: {dailyPnL} \n Unrealized Profit/Lost: {unrealizedPnL} \n Realized Profit/Lost: {realizedPnL}" )

#Creates the instances
ib = InteractiveBrokers()
#Conectarnos a OB TWS o IB Gateway (By default, TWS uses the 7497 port and the Gateway uses the port 4001)
ib.connect(host="127.0.0.1", port=7497, clientId=1)
api_thread = threading.Thread(target=ib.run)
api_thread.start()

print("Active connection", ib.isConnected())

# request account information
ib.reqAccountSummary(requOd=1, groupName="All", tags="$LEDGER")

#request account profit/lost into the account we need to run the befored code to show which one it is
ib.reqPnL(reqId=2, account="", modelCode="")


# Reminder:
#   - Most methods of the EWrapper base class must be overridden for correct information processing.