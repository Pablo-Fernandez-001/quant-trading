# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 12:53:36 2026

@author: pabda
"""

# Import libs
from ibapi.client import EClient # Comunication to Interactive Brockers (IB)
from ibapi.wrapper import EWrapper # That one gets the servers answer and process them
import threading

# create class
class InteractiveBrockers(EClient, EWrapper):
    """
        To make easier the API's interaction with InteractiveBrockers
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


#Creates the instances
ib = InteractiveBrockers()
#Conectarnos a OB TWS o IB Gateway (By default, TWS uses the 7497 port and the Gateway uses the port 4001)
ib.connect(host="127.0.0.1", port=7497, clientId=1)
api_thread = threading.Thread(target=ib.run)
api_thread.start()

print("Active connection", ib.isConnected())

# request account information
ib.reqAccountSummary(requOd=1, groupName="All", tags="$LEDGER")


# Reminder:
#   - Ensure that IB TWS or IB Gateway is running and configured to accept API connections. Without this,
#     the connection from the Python script will not work.
#   - Check the port settings:
#       * TWS Live Trading: 7496
#       * TWS Paper Trading: 7497
#       * Gateway Live Trading: 4001
#       * Gateway Paper Trading: 4002
#   - You must enable the "Enable ActiveX and Socket Clients" option in TWS.
#   - You must disable the "Read-Only API" option.