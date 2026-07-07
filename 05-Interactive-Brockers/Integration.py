# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 15:55:51 2026

@author: pabda
"""

# -*- coding: utf-8 -*-
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
    Class that makes the interaction with the InteractiveBrokers API easier.
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
        Method that receives real-time prices, delayed data.
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


# Execute
if __name__ == "__main__":

    # Create class instance
    ib = InteractiveBrokers()

    # Connect to IB TWS or IB Gateway
    # By default, TWS uses port 7497 and Gateway uses port 4001
    ib.connect(host="127.0.0.1", port=7497, clientId=1)

    # Start thread that will run the IB event interface
    api_thread = threading.Thread(target=ib.run)
    api_thread.start()

    # Wait for the connection to be established
    time.sleep(1)

    print("Active Connection:", ib.isConnected())


    # Request account information
    ib.reqAccountSummary(reqId=1, groupName="All", tags="$LEDGER")


    # Create a contract for Apple stock, AAPL
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    ib.reqContractDetails(reqId=1, contract=contract)


    # Request historical data for a stock, AAPL
    end_date = ""

    ib.reqMarketDataType(3)

    ib.reqHistoricalData(
        reqId=1,
        contract=contract,
        endDateTime=end_date,
        durationStr="5 Y",
        barSizeSetting="1 day",
        whatToShow="TRADES",
        useRTH=1,
        formatDate=1,
        keepUpToDate=False,
        chartOptions=[]
    )

    time.sleep(1)

    prices_df = pd.DataFrame(ib.prices[1]).set_index("Date")
    prices_df.index = pd.to_datetime(prices_df.index)

    print(prices_df)


    # Request streaming price data, tick data
    ib.reqMarketDataType(3)  # Market data type 3 means delayed data

    ib.reqMktData(1, contract, "", False, False, [])

    # Wait to receive data, streaming, and keep the program running
    time.sleep(10)

    # Cancel streaming request
    ib.cancelMktData(1)


    # Create a market order to buy 100 Apple shares, AAPL
    order = Order()
    order.action = "BUY"
    order.totalQuantity = 100
    order.orderType = "MKT"
    order.eTradeOnly = ""
    order.firmQuoteOnly = ""

    # Request last valid Id
    ib.reqIds(-1)

    time.sleep(1)

    ib.placeOrder(
        orderId=ib.nextOrderId,
        contract=contract,
        order=order
    )


    # Request account Profit/Loss
    ib.reqPnL(
        reqId=1,
        account="Account.No",
        modelCode=""
    )


    # Disconnect from IB
    ib.disconnect()

    print("Active Connection:", ib.isConnected())