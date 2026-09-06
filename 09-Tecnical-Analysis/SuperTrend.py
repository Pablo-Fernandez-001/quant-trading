# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 19:21:45 2026

@author: pabda
"""

#import libs
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.pyplot as plt

# Super Trend indicator
def SuperTrend(df: pd.DataFrame, length: int = 14, factor: float = 3.0) -> pd.DataFrame:
    """
    SuperTrend is a trend-following indicator. It plots a line on the candlestick chart; depending on the color,
    it indicates whether the trend is negative (a red line above the candles) or positive (a green line below the candles).
    Both lines can serve as support levels (green line) or resistance levels (red line).
    
    How to Trade It:
        
        The easiest way to trade using SuperTrend is to take positions based on the trend. Buy when the line is green (bullish)
        and short sell when the line is red (bearish). SuperTrend is often used as a complementary tool alongside other indicators.
        One common strategy is to combine SuperTrend with the RSI. If there is a trend change (from bullish to bearish on SuperTrend)
        and the RSI crosses below the 50 level, a short position can be opened on the asset. Conversely, if there is a trend change
        (from bearish to bullish on SuperTrend) and the RSI crosses above 50, a long position can be opened.
        
    Parameters:
    -----------
    param : pd.DataFrame : df : Historical asset data.
    -----------
    param : int : length : Window used for the ATR calculation within SuperTrend (default is 14).
    -----------
    param : float : factor : ATR multiplier (default is 3.0).
    
    Output:
    -----------
    return : pd.DataFrame : SuperTrend calculation.
    """
    
    # Calculate the True Range's Indicator
    High, Low, Close = df["High"], df["Low"], df["Close"]
    High_minus_Low = High - Low
    prev_close = Close.shift(periods=1)
    High_minus_prev_close = abs(High - prev_close)
    Low_minus_prev_close = abs(Low - prev_close)
    #True Range
    TR = pd.concat([High_minus_Low, High_minus_prev_close, Low_minus_prev_close], axis=1).max(axis=1)
    
    # Calculates ATR (Average True Range)
    ATR = TR.ewm(alpha = 1 / length, adjust=False).mean()
    
    #Basic values
    mid_value = (High + Low) / 2
    BasicUpperB = mid_value + factor * ATR
    BasicLowerB = mid_value - factor * ATR
    FinalUpperB = BasicUpperB.copy()
    FinalLowerB = BasicLowerB.copy()
    
    #Initializing SuperTrend
    Supertrend = np.zeros(Close.shape[0])
    Trend = np.ones(Close.shape[0], dtype=bool)
    
    for i in range(1, Close.shape[0]):
        #Fitting the final bands
        if BasicUpperB.iloc[i] < FinalUpperB.iloc[i - 1] or Close.iloc[i - 1] > FinalUpperB.iloc[i - 1]:
            FinalUpperB.iloc[i] = BasicUpperB.iloc[i]
        else:
            FinalUpperB.iloc[i] = FinalUpperB.iloc[i - 1]
            
        if BasicLowerB.iloc[i] > FinalLowerB.iloc[i - 1] or Close.iloc[i - 1] < FinalLowerB.iloc[i - 1]:
            FinalLowerB.iloc[i] = BasicLowerB.iloc[i]
        else:
            FinalLowerB.iloc[i] = FinalLowerB.iloc[i - 1]
        
        #Calculate the supertrend to each point
        if i == 1:
            if Close.iloc[i] <= FinalUpperB.iloc[i]:
                Supertrend[i] = FinalUpperB.iloc[i]
                Trend[i] = False
            else:
                Supertrend[i] = FinalLowerB.iloc[i]
                Trend[i] = True
        else:
            if Supertrend[i - 1] == FinalUpperB.iloc[i - 1]:
                if Close.iloc[i] <= FinalUpperB.iloc[i]:
                    Supertrend[i] = FinalUpperB.iloc[i]
                    Trend[i] = False
                else:
                    Supertrend[i] = FinalLowerB.iloc[i]
                    Trend[i] = True
            else:
                if Close.iloc[i] >= FinalLowerB.iloc[i]:
                    Supertrend[i] = FinalLowerB.iloc[i]
                    Trend[i] = True
                else:
                    Supertrend[i] = FinalUpperB.iloc[i]
                    Trend[i] = False
    
    #Deleting unwanted values
    UpTrend = np.where(Trend == True, Supertrend, np.nan)
    DownTrend = np.where(Trend == False, Supertrend, np.nan)
    TrendChange = np.where(pd.Series(Trend, index=df.index) != pd.Series(Trend, index=df.index).shift(1), Supertrend, np.nan)
    
    ST_df = pd.DataFrame(index=df.index)
    ST_df["SuperTrend"] = Supertrend
    ST_df["Bullish Trend"] = UpTrend
    ST_df["Bearish Trend"] = DownTrend
    ST_df["Trend Change"] = TrendChange
    
    return ST_df
    
#Getting Data
file_path = "../data/AMZN.csv"
df = pd.read_csv(file_path, index_col = "Date", parse_dates=True)
#Calculate indicator
sp = SuperTrend(df)
#Plotting
sp_plots = [
    mpf.make_addplot(sp["Trend Change"], label="Trend Change", color="black", secondary_y=False),
    mpf.make_addplot(sp["Bearish Trend"], label="Bearish Trend", color="red", secondary_y=False),
    mpf.make_addplot(sp["Bullish Trend"], label="Bullish Trend", color="green", secondary_y=False)
    ]
mpf.plot(df, type="candle", style="yahoo", volume=True, figsize=(22, 10), addplot=sp_plots, figscale=3.0, title="SuperTrend")
plt.show()

# Reminder:
#   - SuperTrend identifies bullish and bearish trends using ATR-based bands.
#   - The green line represents a bullish trend and the red line represents a bearish trend.
#   - The black line shows the trend change points.