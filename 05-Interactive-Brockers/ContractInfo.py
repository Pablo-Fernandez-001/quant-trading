# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 18:30:06 2026

@author: pabda
"""
#libraries import
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
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
        
    def contractDetails(self, reqId, contractDetails):
        """
            this method returns the active contract details
        """
        
        #print answer
        print("Contract details:\n")
        print(f"Id: {reqId}\n")
        print(f"Contract: {contractDetails}")
        
        return contractDetails
        
#Creates the instances
ib = InteractiveBrockers()
#Conectarnos a OB TWS o IB Gateway (By default, TWS uses the 7497 port and the Gateway uses the port 4001)
ib.connect(host="127.0.0.1", port=7497, clientId=1)
api_thread = threading.Thread(target=ib.run)
api_thread.start()

print("Active connection", ib.isConnected())


#Create a contract for the action
contract = Contract()
contract.symbol = "APPL"
contract.secType = "STK"
#types:
#   "STK": Actions
#   "FUT": Futures
#   "IND": Indexes
#   "CASH": Divisas
#   "BOND": Bonos
contract.exchange = "SMART"
# "SMART": Sistema de Enrutamiento Inteligente
# "NYSE": New York Stock Exchange
# "NASDAQ": National Association of Securities Dealers Automated Quotations
# "AMEX": American Stock Exchange
# "CBOE": Chicago Board Options Exchange
# "FOREX": Foreign Exchange Market
contract.currency = "USD"

# GET DETAILED CONTRACT INFORMATION: Take care if you already connected in the terminal, you must to close that conection before
contract_details = ib.reqContractDetails(reqId=1, contract=contract)

# Close connection
ib.disconnect()

print("Active connection", ib.isConnected())

# Reminder:
#   - The contractDetails() function provides comprehensive details about the asset's contract, making it easier
#     to understand the parameters and characteristics of the requested contract.
#   - Contracts are fundamental to a wide range of operations, such as requesting historical data, executing
#     market orders, and obtaining real-time data. This is due to the vast array of instruments available
#     on Interactive Brokers, which require precise and detailed specifications.