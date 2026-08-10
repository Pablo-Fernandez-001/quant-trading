# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 22:11:45 2026

@author: pabda
"""

#libs impor
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Get data
assets = ["AAPL","MSFT","GOOGL","DIS"]
start_date = "2023-01-01"
end_date = "2024-01-01"
prices = yf.download(tickers=assets, start=start_date, end=end_date, interval="1d")

prices = prices["Close"]
#Sorting by columns
prices = prices[assets]

#Plotting prices
colors = ["red", "green", "blue", "orange"]
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(22,12))
for n, ax in enumerate(axes.flatten()):
    prices[assets[n]].plot(color=colors[n], lw=2, ax=ax, label=assets[n], title=f"Close's prices:{assets[n]}")
    ax.grid()
    ax.legend()
plt.tight_layout()
plt.show()

# getting returns
returns = prices.pct_change()
# Retunrs and Daily Returns
average_daily_returns = returns.mean()
average_daily_volatility = returns.std()

# Merge in a Dataframe
daily_returns_volatility = pd.DataFrame(columns=["Average Daily Returns","Average Daily Volatility"], index=assets)
daily_returns_volatility["Average Daily Returns"] = average_daily_returns
daily_returns_volatility["Average Daily Volatility"] = average_daily_volatility
print(daily_returns_volatility)

#Annualized Data
annualized_returns_volatility = pd.DataFrame(
    columns=["Average Annualized Returns", "Average Annualized Volatility"],
    index=assets
)

annualized_returns_volatility["Average Annualized Returns"] = average_daily_returns * 252
annualized_returns_volatility["Average Annualized Volatility"] = average_daily_volatility * np.sqrt(252)

print(annualized_returns_volatility)

# Creating investment portfolio

# 1st Portfolio: 25% AAPL, 25% MSFT, 25% GOOGL, 25% DIS
appl_percent = 0.25
msft_percent = 0.25
googl_percent = 0.25
dis_percent = 0.25
portfolio1 = returns["AAPL"] * appl_percent + returns["MSFT"] * msft_percent + returns["GOOGL"] * googl_percent + returns["DIS"] * dis_percent
print(f"1st Portfolio \n{portfolio1}")

# 2nd Portfolio: 30% AAPL, 30% MSFT, 30% GOOGL, 10% DIS
appl_percent = 0.3
msft_percent = 0.3
googl_percent = 0.3
dis_percent = 0.1
portfolio2 = returns["AAPL"] * appl_percent + returns["MSFT"] * msft_percent + returns["GOOGL"] * googl_percent + returns["DIS"] * dis_percent
print(f"2nd Portfolio \n{portfolio2}")

# 3rd Portfolio: 15% AAPL, 25% MSFT, 40% GOOGL, 20% DIS
appl_percent = 0.15
msft_percent = 0.25
googl_percent = 0.4
dis_percent = 0.2
portfolio3 = returns["AAPL"] * appl_percent + returns["MSFT"] * msft_percent + returns["GOOGL"] * googl_percent + returns["DIS"] * dis_percent
print(f"3rd Portfolio \n{portfolio3}")

# 4th Portfolio: 33% AAPL, 33% MSFT, 33% GOOGL, 1% DIS
appl_percent = 0.33
msft_percent = 0.33
googl_percent = 0.33
dis_percent = 0.01
portfolio4 = returns["AAPL"] * appl_percent + returns["MSFT"] * msft_percent + returns["GOOGL"] * googl_percent + returns["DIS"] * dis_percent
print(f"4th Portfolio \n{portfolio4}")

# Merging annualized returns and volatility for each portfolio and existing data
annualized_returns_volatility.loc["Portfolio 1"] = [
    portfolio1.mean() * 252,
    portfolio1.std() * np.sqrt(252)
]

annualized_returns_volatility.loc["Portfolio 2"] = [
    portfolio2.mean() * 252,
    portfolio2.std() * np.sqrt(252)
]

annualized_returns_volatility.loc["Portfolio 3"] = [
    portfolio3.mean() * 252,
    portfolio3.std() * np.sqrt(252)
]

annualized_returns_volatility.loc["Portfolio 4"] = [
    portfolio4.mean() * 252,
    portfolio4.std() * np.sqrt(252)
]

print(annualized_returns_volatility)

# Plotting each asset and portfolio: expected returns vs volatility
plt.figure(figsize=(22,12))

plt.plot(
    annualized_returns_volatility["Average Annualized Volatility"],
    annualized_returns_volatility["Average Annualized Returns"],
    "ro",
    ms=20
)

# Adding labels
for label in annualized_returns_volatility.index:
    plt.text(
        annualized_returns_volatility.loc[
            label,
            "Average Annualized Volatility"
        ],
        annualized_returns_volatility.loc[
            label,
            "Average Annualized Returns"
        ],
        label,
        ha="left",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        rotation=45
    )

plt.xlabel(r"Volatility $\sigma$", size=25)
plt.ylabel(r"Annual Returns $E[r]$", size=25)
plt.grid()
plt.show()

# Reminder:
#   - Diversification can reduce risk exposure and improve performance.
#   - Diversification can protect us against specific market events that affect a group of assets.