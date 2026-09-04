# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 02:35:56 2026

@author: pabda
"""

# Import libs
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# List of stock tickers that we will evaluate
tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
    "JNJ", "SQ", "PYPL", "META", "NFLX"
]


results = []

for ticker in tickers:
    
    # Get the stock financial data
    stock = yf.Ticker(ticker)
    
    try:
        # Get the latest stock price
        last_price = stock.info["currentPrice"]
        
        # Get Net Income and EBIT
        financials = stock.financials
        
        net_income = financials.loc["Net Income"][0]  # Net Income
        
        ebit = financials.loc["EBIT"][0]  # Earnings Before Interest and Taxes
        
        
        # Calculate ROC
        total_assets = stock.balance_sheet.loc["Total Assets"].iloc[0]
        
        current_liabilities = stock.balance_sheet.loc[
            "Current Liabilities"
        ].iloc[0]
        
        working_capital = total_assets - current_liabilities
        
        roc = (ebit / working_capital) * 100
        
        
        # Calculate Earnings Yield
        earnings_yield = (ebit / last_price) * 100
        
        
        # Calculate P/E Ratio
        pe_ratio = (
            last_price
            / (net_income / stock.info["sharesOutstanding"])
        )
        
        
        # Add the results to the list
        results.append({
            "Ticker": ticker,
            "ROC": roc,
            "Earnings Yield": earnings_yield,
            "P/E Ratio": pe_ratio
        })
        
        
    except Exception as error:
        print("Error getting data for:", ticker, error)


# Create a DataFrame with the results
results = pd.DataFrame(
    data=results,
    columns=[
        "Ticker",
        "ROC",
        "Earnings Yield",
        "P/E Ratio"
    ]
).set_index("Ticker")


# Calculate Ranking
results["Ranking"] = (
    results["ROC"].rank(
        ascending=False,
        na_option="bottom"
    )
    +
    results["Earnings Yield"].rank(
        ascending=False,
        na_option="bottom"
    )
)


# Sort by Ranking and P/E Ratio
results = results.sort_values(
    by=["Ranking", "P/E Ratio"],
    ascending=[True, False]
)


# Show the best options according to Greenblatt's strategy
print("Best Stocks According to the Magic Formula:")
print(results)



# Simulate Investment Strategy


# Optimal Assets (According to the Magic Formula)
main_assets = yf.download(
    tickers=list(results.index[:5]),
    start="2024-01-01",
    end="2024-07-01"
)["Close"]


main_assets_return = (
    main_assets
    .pct_change()
    .mean(axis=1)
)


main_assets_return_performance = (
    1 + main_assets_return
).cumprod()



# Less Optimal Assets (According to the Magic Formula)
secondary_assets = yf.download(
    tickers=list(results.index[5:]),
    start="2024-01-01",
    end="2024-07-01"
)["Close"]


secondary_assets_return = (
    secondary_assets
    .pct_change()
    .mean(axis=1)
)


secondary_assets_return_performance = (
    1 + secondary_assets_return
).cumprod()



# Plot returns
plt.figure(figsize=(22, 12))

main_assets_return_performance.plot(
    label="Optimal Assets (Magic Formula)",
    lw=3,
    color="green"
)

secondary_assets_return_performance.plot(
    label="Secondary Assets (Magic Formula)",
    lw=3,
    color="red"
)

plt.legend()
plt.grid()
plt.show()



# Reminder:
#   - The Magic Formula selects stocks using 2 key metrics:
#     Return on Capital (ROC) and Earnings Yield (EY).
#
#   - Stocks are ranked according to these criteria.
#
#   - Companies with the lowest combined ranking scores
#     are considered the best investment opportunities.