# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 11:10:27 2026

@author: pabda
"""

# Import libs
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import threading
import pandas as pd
import time


# Define class
class InteractiveBrokers(EClient, EWrapper):

    """
    Class that makes the interaction with the Interactive Brokers API easier.
    """

    def __init__(self) -> None:

        """
        Constructor.
        """

        # Initialize Client
        EClient.__init__(self, self)

        # Attributes
        self.prices = {}
        self.nextOrderId = None


    def error(self, reqId, errorCode, errorString):

        """
        Error handling function.
        """

        print(f"Error {reqId} {errorCode} {errorString}")


    def accountSummary(self, reqId, account, tag, value, currency):

        """
        Receives account information.
        """

        print(f"Account Summary - Account: {account}, Tag: {tag}, Value: {value}, Currency: {currency}")


    def contractDetails(self, reqId, contractDetails):

        """
        Returns the contract details of an asset.
        """

        print("Contract Details:\n")
        print(f"Id: {reqId}\n")
        print(f"Contract: {contractDetails}")


    def historicalData(self, reqId, bar):

        """
        Receives the historical data of an asset and saves it in a dictionary.
        """

        data = {
            "Date": bar.date,
            "Open": bar.open,
            "High": bar.high,
            "Low": bar.low,
            "Close": bar.close,
            "Volume": bar.volume
        }

        if reqId not in self.prices:
            self.prices[reqId] = []

        self.prices[reqId].append(data)


    def historicalDataEnd(self, reqId, start, end):

        """
        Method called once all historical data has been received.
        """

        print(f"Data downloaded for Id: {reqId}, In the period: {start}-{end}")


    def tickPrice(self, reqId, tickType, price, attrib):

        """
        Method that receives real-time or delayed prices.
        """

        print(f"Tick Price. TickerId: {reqId}, Type: {tickType}, Price: {price}")


    def nextValidId(self, orderId: int):

        """
        Gets the next valid Id to execute an order.
        """

        self.nextOrderId = orderId


    def orderStatus(
        self,
        orderId,
        status,
        filled,
        remaining,
        avgFillPrice,
        permId,
        parentId,
        lastFillPrice,
        clientId,
        whyHeld,
        mktCapPrice
    ):

        """
        Method called every time the order status changes on the server.
        """

        print(f"Order Status - OrderId: {orderId}, Status: {status}")


    def openOrder(self, orderId, contract, order, orderState):

        """
        Method that returns the open orders of our account.
        """

        print("Order Id:", orderId, "Order:", order, "Status:", orderState)


    def pnl(self, reqId: int, dailyPnL: float, unrealizedPnL: float, realizedPnL: float):

        """
        Method that returns the Profit/Loss of the account.
        """

        print(
            "ReqId:", reqId, "\n",
            "Daily Profit/Loss:", dailyPnL, "\n",
            "Unrealized Profit/Loss:", unrealizedPnL, "\n",
            "Realized Profit/Loss:", realizedPnL
        )