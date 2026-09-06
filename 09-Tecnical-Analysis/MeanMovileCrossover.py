# -*- coding: utf-8 -*-

"""
Created on Mon Aug 10 17:56:08 2026

@author: pabda
"""

#import libs
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

#Mobile Mean Crossover
def MA_Crossover(df: pd.DataFrame, fast_length: int=9, slow_length: int = 26, column: str = "Close")-> pd.DataFrame:
    """
    The Moving Average Crossover is a technical indicator that uses two moving averages (MAs) as a trading strategy.
    It is a prime example of what are known as traditional strategies. Traditional strategies are always
    in either a long or short position, meaning they are never out of the market.

    How to Trade It:
        
        Trading with the Moving Average Crossover is quite simple. If the fast moving average crosses
        above the slow moving average, it signals a buying opportunity. If the fast moving average crosses
        below the slow moving average, it signals a selling opportunity. The Moving Average Crossover is frequently used
        alongside other indicators to avoid false signals in low-volatility markets.
        
    Parameters
    ----------
    param : pd.DataFrame : df : Historical data.
    ----------
    param : int : len_rapida : Fast length to use in the MA Crossover calculation (default is 9).
    ----------
    param : int : len_lenta : Slow length to use in the MA Crossover calculation (default is 26).
    ----------
    param : str : column : Column to use in the MA Crossover calculation (default is "Close").
    ----------
    Output:
    ----------
    return : pd.DataFrame : Moving Average Crossover calculation.
    """

    #Calculate
    close = df[column]
    fast_MA = close.rolling(window=fast_length).mean()
    sparced_fast_MA = fast_MA.shift(periods=1)
    slow_MA = close.rolling(window=slow_length).mean()
    sparced_slow_MA = slow_MA.shift(periods=1)

    #Detecting crossovers
    crossover = np.where(((fast_MA > slow_MA) & (sparced_slow_MA > sparced_fast_MA)), 1,
                         np.where(((fast_MA < slow_MA) & (sparced_slow_MA < sparced_fast_MA)), -1, np.nan))

    # Fill all NaNs forward from the crossover points.
    crossover = pd.Series(crossover, index=df.index).ffill()
    MAC = pd.concat([fast_MA, slow_MA, crossover], axis=1)
    MAC.columns=["Fast MA","Slow MA","Crossover"]

    return MAC


#Show an example
data = yf.download("AMZN",start="2019-01-01",end="2024-01-01",interval="1d",multi_level_index=False)

# Calculates strategies for different time periods (Short, Mid, Long term)

st_ma_crossover = MA_Crossover(data, fast_length=9, slow_length=26) #short term
mt_ma_crossover = MA_Crossover(data, fast_length=21, slow_length=50) #mid term
lt_ma_crossover = MA_Crossover(data, fast_length=50, slow_length=200) #long term

#Plot
fig, axes = plt.subplots(nrows=3,ncols=1,figsize=(28,18))
data["Close"].plot(ax=axes[0], label="Close Prices")
st_ma_crossover.plot(secondary_y=["Crossover"],ax=axes[0],title="Sort term with Windows [9,26]")
data["Close"].plot(ax=axes[1], label="Close Prices")
mt_ma_crossover.plot(secondary_y=["Crossover"],ax=axes[1],title="Mid term with Windows [21,50]")
data["Close"].plot(ax=axes[2], label="Close Prices")
lt_ma_crossover.plot(secondary_y=["Crossover"],ax=axes[2],title="Long term with Windows [50,200]")
plt.legend(loc="lower right")
plt.tight_layout()
plt.show()

# Reminder:

# - The MA crossover is a basic yet effective strategy that uses moving averages to identify market
# entry and exit points.
# - It is important to consider the current market context and use multiple timeframes when applying the MA crossover.
# - Confirmation with other technical indicators can improve the accuracy of the indicator's signals.