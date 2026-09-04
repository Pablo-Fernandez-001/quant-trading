# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 01:46:30 2026

@author: pabda
"""

# import libs
import yfinance as yf
import pandas as pd
import time

#Getting market capitalization
def market_cap(asset: str) -> float:
    """
    Gets the market capitalization form an asset

    Parameters
    ----------
    asset : str
        Name for an Asset

    Returns
    -------
    float
        Market capitalization
    """
    
    # Getting data
    asst = yf.Ticker(ticker=asset)
    marketCap = asst.info.get("marketCap", 0)
    
    return marketCap

# Example (Reminder)
if __name__ == "__main__":
    #Own libraries
    from FinancialInstruments import getting_indexes
    
    #Defining index
    index_ticker = "S&P 500"
    file = "index_links.json"
    components = getting_indexes(index_ticker, file)
    #Creating a new column for the marketCap
    components["marketCap"] = 0
    #Extracting his capitalization level
    for n, ticker in enumerate(components["Symbol"]):
        print(f"Information for: {ticker} with index -> {n}")
        marketCap = market_cap(ticker)
        components.loc[n, "marketCap"] = marketCap
        time.sleep(0.5)
    print(components)
    # Save
    components.set_index("Symbol").to_csv(index_ticker + ".csv")
    # Load
    components=pd.read_csv(index_ticker + ".csv", index_col="Symbol")
    
    