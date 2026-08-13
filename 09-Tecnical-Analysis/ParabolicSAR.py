# -*- coding: utf-8 -*-

"""
Created on Tue Aug 11 22:47:54 2026

@author: pabda
"""

# import libs

import pandas as pd
import numpy as np
from copy import deepcopy
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicator: Parabolic SAR

def Parabolic_SAR(df: pd.DataFrame, increase: float = 0.02, max_step: float = 0.20) -> pd.DataFrame:
    """
    The Parabolic SAR indicator is used to determine trend direction and potential
    price reversals. It employs a stop-and-reverse method known as "SAR" to identify
    suitable entry and exit points.

    The indicator uses a system of dots overlaid on a price chart. A reversal occurs 
    when these dots change direction; however, a SAR reversal signal does not 
    necessarily indicate a price reversal. A SAR reversal simply indicates that 
    the price and the indicator have crossed.

    How to Trade It:
        
        The PSAR generates buy or sell signals when the position of the dots shifts 
        from one side of the asset's price to the other. For example, a buy signal 
        occurs when the dots move from above the price to below it, while a sell 
        signal occurs when the dots move from below the price to above it.
        
        PSAR dots are used to set trailing stop-loss orders. For instance, if the 
        price is rising and the PSAR is also rising, the PSAR can serve as a 
        potential exit point for a long position. If the price falls below the 
        PSAR, the long position should be closed.
        
    Parameters:
    -----------
    param : pd.DataFrame : df : Historical asset data.
    -----------
    param : float : increase : Maximum increment used in the Parabolic SAR calculation (default is 0.02).
    -----------
    param : float : max_step : Maximum step used in the Parabolic SAR calculation (default is 0.20).

    Output:
    -----------
    return : pd.DataFrame : Parabolic SAR calculation.
    """

    #Calculate
    data = deepcopy(df)
    High, Low, Close = data["High"].values, data["Low"].values, data["Close"].values
    psar_up, psar_down = np.repeat(np.nan, Close.shape[0]), np.repeat(np.nan, Close.shape[0])
    up_trend = True
    up_trend_high = High[0]
    down_trend_low = Low[0]
    acc_factor = increase
    for i in range(2, Close.shape[0]):
        reversal = False
        max_High = High[i]
        min_Low = Low[i]
        # Upward trend
        if up_trend:
            #Calculates the new PSAR to an Upward trend
            Close[i] = Close[i-1] + (acc_factor * (up_trend_high - Close[i - 1]))
            #Verify if it produces a trend's reversion
            if min_Low < Close[i]:
                reversal = True
                Close[i] = up_trend_high
                down_trend_low = min_Low
                # Reboot the Acelerator's Factor
                acc_factor = increase
            else:
                if max_High > up_trend_high:
                    up_trend_high = max_High
                    acc_factor = min(acc_factor + increase, max_step)
                low1 = Low[i-1]
                low2 = Low[i-2]
                # Fitting the psar if the values fells
                if low2 < Close[i]:
                    Close[i] = low2
                elif low1 < Close[i]:
                    Close[i] = low1
        #Bearish trend
        else:
            #Calculates a new PSAR for a Bearish trend
            Close[i] = Close[i - 1] - (acc_factor * (Close[i - 1] - down_trend_low))
            # Verify if it produces a trend's reversion
            if max_High > Close[i]:
                #Indicates if it produces a Reversion
                reversal = True
                Close[i] = down_trend_low
                up_trend_high = max_High
                # Reboot the Aceleration's Factor
                acc_factor = increase
            else:
                if min_Low < down_trend_low:
                    down_trend_low = min_Low
                    acc_factor = min(acc_factor + increase, max_step)
                high1 = High[i-1]
                high2 = High[i-2]
                #Fitting the PSAR in case the values going up
                if high2 > Close[i]:
                    Close[i] = high2
                elif high1 > Close[i]:
                    Close[i] = high1
                    
        # Updates the trend's direction
        up_trend = up_trend != reversal
        
        # Updates the PSAR's dots
        if up_trend:
            psar_up[i] = Close[i]
        else:
            psar_down[i] = Close[i]
        
    data["PSAR"] = Close
    data["Upper Trend"] = psar_up
    data["Bearer Trend"] = psar_down

    return data[["PSAR","Upper Trend","Bearer Trend"]]


# Getting Data

file_path = "../data/AMZN.csv"
df = pd.read_csv(file_path, index_col = "Date", parse_dates=True)

# Calculates the indicator

p_sar = Parabolic_SAR(df)

# Plots

psar_plots = [
mpf.make_addplot(p_sar["Upper Trend"], label="Upper Trend", color="green", type="scatter"),
mpf.make_addplot(p_sar["Bearer Trend"], label="Bearer Trend", color="red", type="scatter"),
]
mpf.plot(df, type="candle", style="yahoo", volume=True, figsize=(22,10), addplot=psar_plots, figscale=3.0, title="Parabolic SAR")
plt.show()

# Reminder:
#   - The Parabolic SAR identifies trends and potential reversals using dots above or below the price.
#   - SAR dots can serve as entry or exit signals depending on their position relative to the price.