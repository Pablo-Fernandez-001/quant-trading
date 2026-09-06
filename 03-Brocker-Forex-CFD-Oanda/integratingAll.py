# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 00:06:05 2026

@author: pabda
"""
# Import libraries
import tpqoa
import pandas as pd
import time
import threading


# Define class
class Oanda:
    
    """
    Class that makes the interaction with the OANDA API easier.
    """
    
    def __init__(self, conf_file: str) -> None:
        
        """
        Constructor.
        """
        
        self.conf_file = conf_file
        self.oanda_api = tpqoa.tpqoa(conf_file=self.conf_file)
        self.prices = {}   
        self.streaming = {}
        self.stop_streaming = False
        
        
    def account_info(self) -> dict:
        
        """
        Returns the information related to the account.
        """
        
        return self.oanda_api.get_account_summary()
    
    
    def instruments(self) -> list:
        
        """
        Returns a list with the instruments available in OANDA.
        """
        
        return self.oanda_api.get_instruments()
    
    
    def get_data(self, tickers, start, end, granularity) -> None:
        
        """
        Gets historical data for one ticker or a group of them.
        """
        
        # Download data
        tickers = [tickers] if not isinstance(tickers, list) else tickers
        
        for instrument in tickers:
            prices = self.oanda_api.get_history(instrument=instrument, start=start, end=end, 
                                                granularity=granularity, price="M")
            self.prices[instrument] = prices
            
    
    def streaming_data(self, ticker: str, n: int) -> None:
        
        """
        Method that processes the received streaming data.
        """
    
        # Check if the ticker already exists
        if ticker not in self.streaming:
            self.streaming[ticker] = pd.DataFrame(columns=["time", "bid", "ask"])
        counter = 0
        while counter <= n:
            time_, bid, ask = self.oanda_api.get_prices(instrument=ticker)
            print(f"Time: {time_}, Bid: {bid}, Ask: {ask}")
            new_record = pd.DataFrame([[time_, bid, ask]], columns=["time", "bid", "ask"])
            # Concatenate
            self.streaming[ticker] = pd.concat([self.streaming[ticker], new_record], ignore_index=True)
            # Check if execution should stop
            if self.stop_streaming:
                break
            else: 
                time.sleep(1)
            # Increase counter
            counter += 1
            
            
    def parallel_streaming_data(self, ticker: str, n: int) -> None:
        
        """
        Function that parallelizes the execution of the 'streaming_data' method.
        """
       
        # Parallelize
        threading.Thread(target=self.streaming_data, args=(ticker, n)).start()


# Test
if __name__ == "__main__":
    # Instantiate
    oanda = Oanda(conf_file="config.cfg")
    # Get Account Information
    print("\nAccount Information:\n")
    print(oanda.account_info())
    # Get Instruments
    print("\nInstruments:\n")
    instruments = oanda.instruments()
    for name, ticker in instruments:
        print("Name:", name, "Ticker:", ticker)
    # Get Historical Data
    print("\nHistorical Information\n:")
    oanda.get_data(tickers=["EUR_USD", "XAU_USD"], start="2023-01-01", end="2024-01-01", granularity="D")
    print(oanda.prices["EUR_USD"])
    print(oanda.prices["XAU_USD"])
    # Data Streaming
    print("\nData Streaming:\n")
    oanda.streaming_data(ticker="EUR_USD", n=10)    
    print(oanda.streaming["EUR_USD"])
    # Parallelized Data Streaming
    print("\nParallelized Data Streaming:\n")
    oanda.parallel_streaming_data(ticker="EUR_USD", n=1000000)
    time.sleep(10)
    oanda.stop_streaming = True
    # Execute Orders
    print("\nExecute Orders\n:")
    oanda.oanda_api.create_order(instrument="EUR_USD", units=1000, ret=True)