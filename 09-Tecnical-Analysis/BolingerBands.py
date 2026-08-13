# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 22:50:29 2026

@author: pabda
"""

# Import libs
import pandas as pd
from copy import deepcopy
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf # That helps to plot the japanesse candles

# Bolinger's Bands function
def Bolinger_Bands(df: pd.DataFrame, length: int =20, std_dev : float = 2.0, columns: str = "Close") -> pd.DataFrame:
    """
    Bollinger Bands are a technical analysis tool used to generate overbought or oversold signals. They
    consist of three lines: a simple moving average (known as the middle band) and an upper and lower band. The upper
    and lower bands are typically set at +/- 2 standard deviations from a 20-day simple moving average.
    
    How to Trade Using Them:
        
        When the asset's price breaks below the lower Bollinger Band, prices may have fallen
        too far, and a rebound is likely. Conversely, when prices break above the upper band, the market
        may be overbought, and a correction is likely.
        
        Using the bands as overbought/oversold indicators relies on the concept of price mean reversion.
        Mean reversion assumes that if prices deviate substantially from the mean or average, they will eventually return
        to the average price.
        
    Parameters
    ----------
    param : pd.DataFrame : df : Historical asset data.
    ----------
    param : int : length : Window to use for the Bollinger Bands calculation (default is 20).
    ----------
    param : float : std_dev : Number of standard deviations to use for the Bollinger Bands calculation (default is 2.0).
    ----------
    param : str : column : Column to use for the Bollinger Bands calculation (default is "Close").
    
    Output:
    ----------
    return : pd.DataFrame : Bollinger Bands calculation.
    """
    
    #Calculate
    data = deepcopy(df)
    rolling = data[columns].rolling(window=length)
    data["MA"] = rolling.mean()
    std_bands = std_dev * rolling.std(ddof=0)
    data["BB_Up"] = data["MA"] + std_bands
    data["BB_Lw"] = data["MA"] - std_bands
    
    return data[["BB_Up", "MA","BB_Lw"]]

# Getting data
df = yf.download(tickers="PYPL",start="2019-01-01",end="2024-01-01",interval="1d",multi_level_index=False)
# Calculates Bollinger Bands
bb = Bolinger_Bands(df,length=20,std_dev=2.0)
#Plotting
bb_plot = mpf.make_addplot(bb)
mpf.plot(df, type="candle", style="yahoo", volume=True, figsize=(22, 10), addplot=bb_plot, figscale=2.0, title="Bollinger Bands")
plt.show()

#Recordatorio:
# - Las Bandas de Bollinger pueden indicar niveles de sobrecompra y sobreventa cuando los precios tocan o cruzan
# la banda superior e inferior, respectivamente.
# - La reversión a la media indica que los precios tienden a regresar a un nivel promedio después de tocar las Bandas
# de Bollinger, lo que puede ayudar a identificar oportunidades de trading.