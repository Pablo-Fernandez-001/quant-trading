# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 20:23:06 2026

@author: pabda
"""

# Import Libs
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt


#get hist data
tickers_list = ["AMZN", "TSLA", "MSFT", "NFLX", "META", "PYPL"]
data = {}
start_date = "2023-01-01"
end_date = "2024-01-01"
for ticker in tickers_list:
    data[ticker] = yf.download(ticker, start=start_date, end=end_date, interval="1d")
    
#Plotting prices (one by one)
plt.figure(figsize=(22,12))
for ticker in tickers_list:
    data[ticker]["Close"].plot(label=ticker)
plt.legend()
plt.grid()
plt.show()

#Plotting all prices (in one)
fig, ax = plt.subplots(figsize=(22, 12))

for ticker in tickers_list:
    prices = data[ticker]["Close"]

    # If yfinance returns only one data column
    if isinstance(prices, pd.DataFrame):
        prices = prices.squeeze()

    prices.plot(
        ax=ax,
        label=ticker
    )

ax.set_title("Historical Close Pricing")
ax.set_xlabel("Date")
ax.set_ylabel("USD Prices")
ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()

# Daily Returns
returns = pd.DataFrame(columns=tickers_list)
for ticker in tickers_list:
    returns[ticker] = data[ticker]["Close"].pct_change()
print(returns)

#Plotting returns
returns.plot(figsize=(22,12),title="Assets' Returns")
plt.show()

# Getting Annualized Retunrs
average_daily_returns = returns.mean(axis=0)
annualizated_returns = average_daily_returns * 252
print(f"Annulizated Returns for each asset \n{annualizated_returns}\n")


# Getting volatility
average_daily_volatility = returns.std(axis=0)
annualizated_volatility = average_daily_volatility * np.sqrt(252) # The volatility increases by the squared root, not with a summation
print(f"Annual Volatility for each asset: \n {annualizated_volatility}\n")


#plotting returns vs volatility
x_values = annualizated_volatility.values
y_values = annualizated_returns.values
plt.figure(figsize=(22,12))
plt.plot(x_values, y_values,"ro", ms=20)
# Add labels
for ticker in tickers_list:
    x = annualizated_volatility[ticker]
    y = annualizated_returns[ticker]
    plt.text(x,y, ticker, ha="left",va="bottom",fontsize=10,fontweight="bold",rotation=45)
plt.xlabel("Volatility $\sigma$",size=25)
plt.ylabel("Annual Retunrs $E[r]$", size=25)
plt.grid()
plt.show()

# Reminder:
#   - A higher expected return generally entails assuming a higher level of risk.
#   - Asset diversification within a portfolio can significantly reduce risk,
#     enabling similar returns to be achieved with lower volatility.