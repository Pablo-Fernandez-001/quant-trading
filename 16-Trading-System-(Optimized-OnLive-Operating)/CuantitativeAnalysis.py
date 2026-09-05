# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 02:57:28 2026

@author: pabda
"""

# Import libs
import yfinance as yf
import pandas as pd
import numpy as np
from hmmlearn import hmm

# Hidden States from Markov Model
def Hidden_States(df: pd.DataFrame, n_continuity: int = 25) -> dict:
    
    """
    Detects hidden market states in a time series using a Gaussian Hidden Markov Model.

    Parameters
    ----------
    df : pd.DataFrame
        Historical market data containing at least the Close, High, and Low columns,
        used to calculate logarithmic returns and the price range of each candle.

    n_continuity : int
        Number of consecutive observations used to identify the trend direction
        of the hidden states. Default is 25.

    Returns
    -------
    dict
        Dictionary containing the identified bullish and bearish hidden states,
        along with the trained Gaussian Hidden Markov Model.
    """
    
    # Add logarithmic returns and the daily range of each candle
    df["log_r"] = np.log(df["Close"] / df["Close"].shift(periods=1))
    df["range"] = df["High"].div(df["Low"]) - 1
    
    # Define the model with 2 hidden states
    model = hmm.GaussianHMM(n_components=2, covariance_type="full", random_state=1)
    
    # Fit the model
    data = df[["log_r", "range"]].dropna()
    model.fit(data)
    
    # Predict
    hidden_states = model.predict(data)
    
    # Separate Hidden States
    Close = df.dropna()["Close"]
    state0 = Close.where(hidden_states==0, np.nan)
    state1 = Close.where(hidden_states==1, np.nan)
    
    states = {"bullish": "", "bearish": ""}
    
    # Iterate through the rows of any state (state0 or state1)
    for i in range(state0.shape[0] - n_continuity):
        sub_state0 = state0.iloc[i: i + n_continuity].dropna()
        # Check if there are 25 continuous data points
        if sub_state0.shape[0] == n_continuity:
            # Fit Regression to know the slope
            params = np.polyfit(x=sub_state0, y=range(0, n_continuity), deg=1)
            slope = params[0]
            if slope > 0:
                states["bullish"] = state0
                states["bearish"] = state1
            else:
                states["bullish"] = state1
                states["bearish"] = state0
            # Stop execution
            break
       
    return {"states": states, "model": model}

# Example (Reminder)
if __name__ == "__main__":
    # Getting Data
    df = yf.download("SPY", start="2021-01-01", end="2024-01-01", interval="1d")
    
    # Fixing yfinance MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    
    # Finding states
    model_states = Hidden_States(df)
    states = model_states["states"]
    model = model_states["model"]
    print(f"States: {states}")
    print(f"Model: {model}")