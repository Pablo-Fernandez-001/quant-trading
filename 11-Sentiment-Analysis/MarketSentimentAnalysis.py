# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 20:02:21 2026

@author: pabda
"""

#import libs
import pandas as pd
import requests
from bs4 import BeautifulSoup # Converts the http request in an html's file
from datetime import datetime
from fake_useragent import UserAgent # pip install fake_useragent, simulates fake users to don't block the queries on the platfomr
import seaborn as sns
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from warnings import filterwarnings
filterwarnings("ignore")

# We're gonna use finviz (finviz.com) to import all the news, to show all the news, we only uses the Ticker name of the asset
# It's only by assets.

#finviz url
url = "https://finviz.com/stock?t={}&p=d"
tickers = ["AMZN","MSFT","TSLA","NVDA","GOOGL"]

#Extract html
extractions = []
for ticker in tickers:
    #Creating fake usesrs to realizing requests (avoiding page-blocks)
    ua = UserAgent()
    header = {"User-Agent": str(ua.chrome)}
    #Petition
    r = requests.get(url=url.format(ticker), headers=header)
    soup = BeautifulSoup(r.content, "html5lib")
    # Locate news table
    news_table = soup.find(id="news-table")
    # Locate each individual new
    news = news_table.findAll(name="tr")
    firstone = news[0].find("a", attrs={"class":"tab-link-news"}).text
    firstone_date = news[0].find("td").text.replace("\n","").strip()
    print(f"Each individual new (just the firstone to view if it works) {firstone}, \nand date: {firstone_date}")
    #Save news and headliners
    for new in news:
        news_data = new.find("a", attrs={"class":"tab-link-news"})
        headliner = news_data.text
        news_dates_hours = new.find(name="td").text.replace("\n","").strip().split()
        # Formatting the right date:
        if len(news_dates_hours) == 2:
            date = news_dates_hours[0]
            hour = news_dates_hours[1]
            if date.lower == "today":
                date = datetime.now().strftime("%b-%d-%y")
        else:
            hour = news_dates_hours[0]
        
        extractions.append([ticker, date, hour, headliner])

# Convert into a Dataframe the extractions
news = pd.DataFrame(data=extractions, columns=["Ticker","Date","Hour","Headliner"])
news["Date"] = pd.to_datetime(news["Date"], format="%b-%d-%y")

#Getting sentiment
sia = SentimentIntensityAnalyzer()
news["Sentiment"] = news["Headliner"].apply(lambda x: sia.polarity_scores(x)["compound"])

# Clustering all data by ticker and by day
clustered_news = news[["Ticker","Date","Sentiment"]].groupby(["Ticker","Date"]).mean()
clustered_news.reset_index(inplace=True)

#Making Graph
plt.figure(figsize=(14,7))
sns.barplot(x="Date", y="Sentiment", hue="Ticker", data=clustered_news)
plt.xlabel("Date", size=20)
plt.ylabel("Average Sentiment", size=20)
plt.title("Average New's Sentiment by Ticker and Date", size = 20)
plt.xticks(rotation=0)
plt.legend()
plt.tight_layout()
plt.show()

# Reminder:
#   - Sentiment analysis is strongly correlated with asset movements in financial markets.
#   - Sentiment analysis may be limited to assets that are popular among traders and investors.