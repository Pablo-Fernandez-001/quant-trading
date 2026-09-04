# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 02:47:28 2026

@author: pabda
"""

# import libs
import yfinance as yf
import pandas as pd
import time


# Defining function
def Magic_Formula(tickers: list) -> pd.DataFrame:
    """
    SUMMARY.

    Calculates the Magic Formula Metodology for an assets dataset
    ----------
    tickers : list
        Tickers name to use

    Returns
    -------
    pd.DataFrame
        magic formula for each ticker
    """
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

        # Sleeping to avoid the server blocking
        time.sleep(1)
        
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
    
    return results

# Example (Reminder)
if __name__ == "__main__":
    # Load Data
    df_file = "S&P 500.csv"
    df = pd.read_csv(df_file, index_col="Symbol")
    # Sorting on base the capitalization (keeping the 100 grower)
    df = df.sort_values(by="marketCap", ascending=False).iloc[:100]
    # Finding the bes base values on the Magic Formula metodology
    fm = Magic_Formula(tickers=list(df.index))
    print(fm)
    # Save Data
    fm.dropna().to_csv("MagicFormula.csv")