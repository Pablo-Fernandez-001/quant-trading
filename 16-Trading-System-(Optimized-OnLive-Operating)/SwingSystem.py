# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 22:08:08 2026

@author: pabda
"""

#import libs
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
from warnings import filterwarnings
filterwarnings("ignore")

#Own libraries
from FinancialInstruments import getting_indexes
from HistInfo import market_cap
from CuantitativeAnalysis import Hidden_States
from Strategies.Strategy2_SuperTrend import Strategy2

#Defining the Short/Mid-Term Trading System
def Swing_System(download_data: bool = False) -> None:
    
    """
    Runs a short/mid-term swing trading system at one-hour intervals using the largest
    companies in the S&P 500 by market capitalization.
    
    The system optionally downloads and updates the S&P 500 constituents and their
    market capitalization data, or loads the previously stored information from a CSV file.
    It then selects the 30 largest companies and downloads the last 30 days of hourly
    historical market data for each asset.
    
    For each ticker, the system combines a Hidden Markov Model with the SuperTrend strategy
    to confirm the current market direction. A buy or sell signal is generated only when
    the SuperTrend signal agrees with the corresponding bullish or bearish hidden state.
    
    The process runs continuously until it is manually interrupted and repeats the analysis
    once every hour.
    
    Parameters
    ----------
    download_data : bool
        Determines whether the S&P 500 constituents and their market capitalization data
        should be downloaded and recalculated. If False, the system loads the previously
        stored data from the corresponding CSV file. Default is False.
    
    Returns
    -------
    None
        The generated trading signals are printed to the console after each complete
        iteration of the system.
    """
    
    #Recovering assets
    if download_data:
        sp500_assets = getting_indexes(index="S&P 500", file="index_links.json")
        sp500_assets["marketCap"] = 0
        
        #Extracting market capitalization
        for n, ticker in enumerate(sp500_assets["Symbol"]):
            marketCap = market_cap(ticker)
            sp500_assets.loc[n, "marketCap"] = marketCap
            
    else:
        sp500_assets = pd.read_csv("S&P 500.csv")
    
    #Keeping the 30 largest assets
    sp500_assets = sp500_assets.sort_values(by="marketCap", ascending=False)
    sp500_assets = sp500_assets["Symbol"].iloc[:30].tolist()
    
    #Executing the system until manually interrupted
    generated_signals = []
    while True:
        for ticker in sp500_assets:
            
            #Getting data and executing the strategy
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30) #Last 30 days
            
            #Giving the correct format
            end_date = end_date.strftime("%Y-%m-%d")
            start_date = start_date.strftime("%Y-%m-%d")
            
            #Getting historical data
            df = yf.download(tickers=ticker, start=start_date, end=end_date, interval="1h", progress=False)
            
            #Review if data exists
            if df.empty:
                print(f"No Yahoo Finance data available for {ticker} in the selected period.")
                continue
            
            #Fixing yfinance MultiIndex
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            #Review if enough data exists
            if df.shape[0] < 15:
                print(f"Not enough Yahoo Finance data available for {ticker} to calculate the strategies.")
                continue
            
            #Calculating strategies
            hs_m = Hidden_States(df=df, n_continuity=10)
            st2 = Strategy2(df=df)
            current_signal = st2.calculate()
            
            #Review if any signal was generated
            if isinstance(current_signal, dict):
                
                if (current_signal["Trend"] == "Bullish") and pd.notna(hs_m["states"]["bullish"].iloc[-1]):
                    #A bullish signal has been generated
                    generated_signals.append([ticker, "buy"])
                    
                elif (current_signal["Trend"] == "Bearish") and pd.notna(hs_m["states"]["bearish"].iloc[-1]):
                    #A bearish signal has been generated
                    generated_signals.append([ticker, "sell"])
                    
                else:
                    continue
                    
        #Printing generated signals to console
        print(f"Short/Mid-Term System: {generated_signals}")
        
        #Sleeping between each iteration (1 hour)
        time.sleep(60 * 60)
    

#Example (Reminder)
if __name__ == "__main__":
    #Executing system
    Swing_System(download_data=False)