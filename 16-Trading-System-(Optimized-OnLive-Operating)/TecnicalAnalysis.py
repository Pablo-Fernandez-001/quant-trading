# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 01:41:47 2026

@author: pabda
"""

#Import libs
import yfinance as yf
import pandas as pd
#Own libraries
from Strategies.Strategy1_MovingAverageCrossovers import Strategy1
from Strategies.Strategy2_SuperTrend import Strategy2

#Defining function
def Multiple_Strategies(data: pd.DataFrame, **kwargs) -> dict:
    """
    Calculates the current state and internal calculations of multiple trading strategies
    using the same market data.
    
    Parameters
    ----------
    data : pd.DataFrame
        Historical market data used by each trading strategy to calculate its
        indicators and determine whether a trading signal has been generated.
    
    **kwargs : dict
        Optional parameters used to configure each strategy, such as moving average
        windows, indicator lengths, or strategy-specific factors.
    
    Returns
    -------
    dict
        Dictionary containing the current signal and calculated strategy data for
        each evaluated trading strategy.
    """
    
    #Create instances
    est1 = Strategy1(df=data, st_window=kwargs.get("st_window", 9), lt_window=kwargs.get("lt_window",14))
    est2 = Strategy2(df=data, length=kwargs.get("length", 14), factor=kwargs.get("factor",3.0))
    
    #Calculates (shows if we have a signal)
    est1_current_situation = est1.calculate()
    est2_current_situation = est2.calculate()
    
    #Extract all generated calculus
    est1_calculus = est1.strategy_calculation
    est2_calculus = est2.strategy_calculation
    
    #Dictionary return
    return {
            "est1":{"signal": est1_current_situation, "calculus":est1_calculus },
            "est2":{"signal": est2_current_situation, "calculus":est2_calculus }
        }   

# We're using both strategies at the sime (into intraday strategy), like use a merge of both

# Example (Reminder)
if __name__ == "__main__":
    #Getting data
    df = yf.download("AMZN", period="5d", interval="1m")
    
    #Fixing yfinance MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    #Strategies calculus
    strategies_calculus = Multiple_Strategies(data=df)
    print(strategies_calculus)