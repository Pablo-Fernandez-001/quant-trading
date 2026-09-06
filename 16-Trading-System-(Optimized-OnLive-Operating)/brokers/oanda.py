# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 11:09:49 2026

@author: pabda
"""

# Import libs
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
        
        # Reset prices
        self.prices = {}
        
        for instrument in tickers:
            try:
                prices = self.oanda_api.get_history(instrument=instrument, start=start, end=end, 
                                                    granularity=granularity, price="M")
                self.prices[instrument] = prices
                
            except AttributeError as error:
                if "tz_localize" in str(error):
                    print(f"No historical data available for {instrument} in the selected period.")
                    continue
                else:
                    raise
            
    
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