# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 23:05:01 2026

@author: pabda
"""

# Import libs
import pandas as pd
import pandas_ta as pd_ta # pip install pandas-ta
import ta # pip install ta , python -m pip install setuptools==80.10.2
# We can use too ta-lib but it's kind difficult to use it, for that reason we doesn't use it

#Getting data
file_path = "../data/AMZN.csv"
df = pd.read_csv(file_path, index_col = "Date", parse_dates=True)
close = df["Close"]
high = df["High"]
low = df["Low"]
vol = df["Volume"]

# pandas_ta's indicators
ma = pd_ta.ma("sma", close, length=8) #Simple Moving Average
ema = pd_ta.ema(close=close, length=14) #Exponential Moving Average
cci = pd_ta.cci(high=high, low=low, close=close, length=14) #Commodity Channel Index
atr = pd_ta.atr(high=high, low=low, close=close, length=21) #Average True Range
print(f"MA: \n{ma}\nEMA: \n{ema}\nCCI: \n{cci}\nATR: \n{atr}")

#ta's indicators
rsi = ta.momentum.RSIIndicator(close=close, window=14).rsi()
macd = ta.trend.MACD(close=close, window_slow=26, window_fast=12, window_sign=9).macd()
cmf = ta.volume.ChaikinMoneyFlowIndicator(high=high, low=low, close=close, volume=vol).chaikin_money_flow()
print(f"RSI: \n{rsi}\nMACD: \n{macd}\nCMF: \n{cmf}")