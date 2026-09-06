# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 11:05:21 2026

@author: pabda
"""

# Import libs
import fxcmpy
import pandas as pd
import time
import threading
 
 
# Define Class
class FXCM:
 
    """
    Class that makes the interaction with the FXCM API easier.
    """
    
    def __init__(self, token: str) -> None:
        
        """
        Constructor.
        """
        
        self.api_token = token
        self.connection = fxcmpy.fxcmpy(access_token=self.api_token, log_level='error')
        self.prices = {}
        self.streaming = {}
        self.stop_streaming = False
    
    
    def account_info(self) -> dict:
        
        """
        Returns the information related to the account.
        """
        
        return self.connection.get_accounts().T.to_dict()
 
 
    def instruments(self) -> list:
        
        """
        Returns a list with the instruments available in FXCM.
        """
        
        return self.connection.get_instruments()
 
 
    def get_historical_data(self, symbols, start, end, period) -> None:
        
        """
        Gets historical data for one or multiple symbols.
        """
        
        symbols = [symbols] if not isinstance(symbols, list) else symbols
        for symbol in symbols:
            data = self.connection.get_candles(symbol, period=period, start=start, stop=end)
            self.prices[symbol] = data
 
 
    def streaming_data(self, symbol: str, n: int) -> None:
        
        """
        Method that processes streaming data.
        """
        
        # Check if the ticker already exists
        if symbol not in self.streaming:
            self.streaming[symbol] = pd.DataFrame(columns=["date", "bid", "ask"])
            
        counter = 0
        while counter <= n:
            prices = self.connection.get_last_price(symbol)
            date = prices.index[0]
            bid, ask = prices["Bid"], prices["Ask"]
            new_row = pd.DataFrame([[date, bid, ask]], columns=["date", "bid", "ask"])
            self.streaming[symbol] = pd.concat([self.streaming[symbol], new_row], ignore_index=True)
            if self.stop_streaming:
                break
            else:
                time.sleep(1)
            counter += 1
            
    def parallel_streaming(self, symbol: str, n: int) -> None:
        
        """
        Function that parallelizes the execution of the 'streaming_data' method.
        """
        
        threading.Thread(target=self.streaming_data, args=(symbol, n)).start()