# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 15:59:12 2026

@author: pabda
"""

#The first Analysis:
#We're going to use both strategies. If the first one (Moving Averages) generates a crossover,
#the second one confirms it (SuperTrend), or if the second one generates a signal,
#the first one confirms it. It's like merging both strategies into one.
#The second Analysis:
#Applying the same logic together with sentiment analysis, but for assets obtained from Yahoo Finance.

#import libs
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
# Own libraries
from Brokers import Brokers
from TecnicalAnalysis import Multiple_Strategies
from SentimentAnalysis import Market_Sentiment

#Defining the intraday system
def Intraday_System() -> None:
    """
    Runs an intraday trading analysis system at one-minute intervals by retrieving
    market data from OANDA and Yahoo Finance, evaluating multiple technical strategies,
    and incorporating market sentiment analysis for selected stocks.
    
    The system generates buy or sell signals only when the evaluated strategies reach
    a directional consensus. For Yahoo Finance assets, market sentiment is also used
    as an additional confirmation condition.
    
    The process runs continuously until it is manually interrupted.
    
    Returns
    -------
    None
        The generated trading signals are printed to the console after each iteration.
    """
    
    #Brokers instance
    brokers = Brokers()
    #Connect to Oanda
    connection_file = "brokers/credentials/config.cfg"
    brokers.Oanda_Initializing(connection_file)
    #Defining Financial Assets Universe
    assets_tuples = brokers.oanda.instruments()
    #Extracting the instruments
    oanda_assets = [i[1] for i in assets_tuples]
    stock_instruments = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOG"]
    
    #Executing the program until its manual interruption
    while True:
        #Getting Data and Strategy Execution
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1) #Previous day
        yfinance_start_date = end_date - timedelta(days=5) #Previous 5 days
        
        #Giving the right format for Oanda
        oanda_end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S")
        oanda_start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S")
        
        #Getting Oanda data
        brokers.oanda.get_data(tickers=oanda_assets, start=oanda_start_date, end=oanda_end_date, granularity="M1")
        
        #Getting Yahoo Finance data
        df_yfinance = {
            instrument: yf.download(tickers=instrument, start=yfinance_start_date, end=end_date, interval="1m", progress=False)
            for instrument in stock_instruments
            }
        
        #Calculating strategies for Oanda data
        generated_signals = []
        for ticker, data in brokers.oanda.prices.items():
            
            #Review if enough data exists
            if data.empty or data.shape[0] < 15:
                print(f"Not enough Oanda data available for {ticker} in the selected period.")
                continue
            
            #Rename columns
            data.columns = ["Open", "High", "Low", "Close", "Volume", "Complete"]
            
            #Calculate Strategy
            oanda_calculus = Multiple_Strategies(data=data)
            
            #Review if any signal exists
            
            #Strategy 1
            if isinstance(oanda_calculus["est1"]["signal"], dict): #A signal was generated in Strategy 1
                current_tendency = 1 if oanda_calculus["est1"]["signal"]["Tendency"] == "Bullish" else -1
                
                #Review if there is a consensus between both strategies
                if (current_tendency == 1) and (pd.notna(oanda_calculus["est2"]["calculus"]["FinalLowerB"].iloc[-1])):
                    #A bullish signal has been generated
                    generated_signals.append([ticker, "buy"])
                    
                elif (current_tendency == -1) and (pd.notna(oanda_calculus["est2"]["calculus"]["FinalUpperB"].iloc[-1])):
                    #A bearish signal has been generated
                    generated_signals.append([ticker, "sell"])
            
            #Strategy 2
            elif isinstance(oanda_calculus["est2"]["signal"], dict): #A signal was generated in Strategy 2
                current_tendency = 1 if oanda_calculus["est2"]["signal"]["Trend"] == "Bullish" else -1
                
                #Review if there is a consensus between both strategies
                if (current_tendency == 1) and (oanda_calculus["est1"]["calculus"]["Crossover"].iloc[-1] == 1.0):
                    #A bullish signal has been generated
                    generated_signals.append([ticker, "buy"])
                    
                elif (current_tendency == -1) and (oanda_calculus["est1"]["calculus"]["Crossover"].iloc[-1] == -1.0):
                    #A bearish signal has been generated
                    generated_signals.append([ticker, "sell"])
            
            else:
                continue
        
        #Calculating strategies for Yahoo Finance data
        for ticker, data in df_yfinance.items():
            
            #Review if data exists
            if data.empty:
                print(f"No Yahoo Finance data available for {ticker} in the selected period.")
                continue
            
            #Fixing yfinance MultiIndex
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            
            #Review if enough data exists
            if data.shape[0] < 15:
                print(f"Not enough Yahoo Finance data available for {ticker} to calculate the strategies.")
                continue
            
            #Calculate Strategy
            yfinance_calculus = Multiple_Strategies(data=data)
            
            #Getting Market Sentiment for this asset
            sentiment = Market_Sentiment(ticker=ticker)["Sentiment"].iloc[-1]
            
            #Review if any signal exists
            
            #Strategy 1
            if isinstance(yfinance_calculus["est1"]["signal"], dict): #A signal was generated in Strategy 1
                current_tendency = 1 if yfinance_calculus["est1"]["signal"]["Tendency"] == "Bullish" else -1
                
                #Review if there is a consensus between both strategies and market sentiment
                if (current_tendency == 1) and (pd.notna(yfinance_calculus["est2"]["calculus"]["FinalLowerB"].iloc[-1])) and (sentiment >= 0):
                    #A bullish signal has been generated
                    generated_signals.append([ticker, "buy"])
                    
                elif (current_tendency == -1) and (pd.notna(yfinance_calculus["est2"]["calculus"]["FinalUpperB"].iloc[-1])) and (sentiment <= 0):
                    #A bearish signal has been generated
                    generated_signals.append([ticker, "sell"])
            
            #Strategy 2
            elif isinstance(yfinance_calculus["est2"]["signal"], dict): #A signal was generated in Strategy 2
                current_tendency = 1 if yfinance_calculus["est2"]["signal"]["Trend"] == "Bullish" else -1
                
                #Review if there is a consensus between both strategies and market sentiment
                if (current_tendency == 1) and (yfinance_calculus["est1"]["calculus"]["Crossover"].iloc[-1] == 1.0) and (sentiment >= 0):
                    #A bullish signal has been generated
                    generated_signals.append([ticker, "buy"])
                    
                elif (current_tendency == -1) and (yfinance_calculus["est1"]["calculus"]["Crossover"].iloc[-1] == -1.0) and (sentiment <= 0):
                    #A bearish signal has been generated
                    generated_signals.append([ticker, "sell"])
        
        
        #Printing generated signals to console
        print("Intraday System:", generated_signals)
        
        #Sleep for 1 minute between each iteration
        time.sleep(60)
        
 
#Example (Reminder)
if __name__ == "__main__":
    #Execute System
    Intraday_System()