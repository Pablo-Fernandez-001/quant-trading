# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 13:56:03 2026

@author: pabda
"""

#compound annual growth rate
#import libs
import pandas as pd
import numpy as np
import yfinance as yf

#Recover data
df = pd.read_csv("../data/NVDA.csv", index_col="Date")
print("Start date", df.index[0])
print("End date", df.index[-1])

# CAGR
def CAGR(data: pd.DataFrame(), optimized_calculus: bool = True, column: str = "Close") -> float:
    """
    It mesures the annual growth about an invertion during a specific time rate period

    Parameters
    ----------
    data : pd.DataFrame
        param: Historial data from a financial asset
    optimized_calculus : bool, optional
        param: If it's true, going to use the first method to calcualte the metric(By default it's True)
    column : str, optional
        param: Column uset to do the calculus (By default it's False)

    Returns
    -------
    float
        Final grow rate
    """
    
    #Calculate
    n = np.ceil(data.shape[0]/252)
    if optimized_calculus:
        start_value = data[column][0]
        final_value = data[column][-1]
        
        return ((final_value / start_value) ** ( 1 / n ) ) - 1
    else:
        #using the returns
        daily_returns = data[column].pct_change()
        accumulated_returns = (1 + daily_returns).cumprod()
        
        # The optimizated calculus just use the initial value and the final to get the annual rate
        # When que uses returns we focus on the rate calculus from an asset's throughout the return
        # It's a bit slower than the other method, imperceptible, but with a lot of assets it's inneficient
        return (accumulated_returns[-1] ** (1/n))-1
        
# example    
print(f"Compound Annual Growth Rate (optimized) {CAGR(df)}")
print(f"Compound Annual Growth Rate (unoptimized) {CAGR(df, optimized_calculus=False)}")


# Repeating the process with a different instrument TSLA
# Before code -> df = yf.download(tickers="TSLA", start=df.index[0], end=df.index[-1], interval="1d")
# Fixed code:
df = yf.download(
    tickers="TSLA",
    start=df.index[0],
    end=df.index[-1],
    interval="1d",
    auto_adjust=False,
    multi_level_index=False
)
print(f"Compound Annual Growth Rate TSLA (optimized) {CAGR(df)}")
print(f"Compound Annual Growth Rate TSLA (unoptimized) {CAGR(df, optimized_calculus=False)}")


# Reminder:
#   - CAGR is a metric commonly used to measure the annualized growth rate of an investment over
#     a specific period of time.