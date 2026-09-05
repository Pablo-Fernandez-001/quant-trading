# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 03:19:22 2026

@author: pabda
"""

# Import libs
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fake_useragent import UserAgent
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Extract Market Sentiment
def Market_Sentiment(ticker: str) -> pd.DataFrame:
    
    """
    Extracts the market sentiment of a financial asset through its news headlines.

    Parameters
    ----------
    ticker : str
        Ticker symbol of the financial asset whose news headlines will be
        extracted and analyzed.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the average market sentiment grouped by ticker
        and publication date.
    """
    
    # Define FINVIZ url
    url = "https://finviz.com/quote.ashx?t={}&p=d"
    
    # Extract HTML
    extractions = []
    # Create fake users to make requests (avoid blocks)
    ua = UserAgent()
    header = {"User-Agent": str(ua.chrome)}
    # Request
    r = requests.get(url=url.format(ticker), headers=header)
    soup = BeautifulSoup(r.content, "html5lib")
    # Locate news table
    news_table = soup.find(id="news-table")
    # Locate each individual news
    news = news_table.findAll(name="tr")
    
    # Initial date
    date = None
    
    # Save news and headlines
    for new in news:
        news_data = new.find(name="a", attrs={"class":"tab-link-news"})
        headline = news_data.text
        publication_date = new.find(name="td").text.replace("\n", "").strip().split()
        # Give the correct format to the date
        if len(publication_date) == 2:
            date = publication_date[0]
            time = publication_date[1]
            if date.lower() == "today":
                date = datetime.now().strftime("%b-%d-%y")
        else:
            time = publication_date[0]
            
        extractions.append([ticker, date, time, headline])
            
    # Convert to DataFrame
    news = pd.DataFrame(data=extractions, columns=["Ticker", "Date", "Time", "Headline"])   
    news["Date"] = pd.to_datetime(news["Date"], format="%b-%d-%y")
            
    # Get sentiment
    sia = SentimentIntensityAnalyzer()
    news["Sentiment"] = news["Headline"].apply(lambda x: sia.polarity_scores(x)["compound"])    
    
    # Group data by ticker and day
    grouped_news = news[["Ticker", "Date", "Sentiment"]].groupby(["Ticker", "Date"]).mean()
    grouped_news.reset_index(inplace=True)
    
    return grouped_news

# Example (Reminder)
if __name__ == "__main__":
    # Define asset
    ticker = "AMZN"
    # Get sentiment
    sentiment = Market_Sentiment(ticker)
    print(sentiment)