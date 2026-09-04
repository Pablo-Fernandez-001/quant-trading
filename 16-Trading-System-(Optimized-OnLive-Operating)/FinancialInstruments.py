# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 21:22:08 2026

@author: pabda
"""

#import libs
import pandas as pd
import json
import requests
from io import StringIO

# Someone libraries can download the data or scappe the same data, but this libraries has a lot of errors
# or scrappe all page could make a lot of dataframes and that means a lot of searchs.

#wikipedia urls
urls = {
        
    "S&P 500": {"link": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", "index": 0, "country": "United States"},
    "Dow Jones Industrial Average": {"link": "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average", "index": 1, "country": "United States"},
    "NASDAQ-100": {"link": "https://en.wikipedia.org/wiki/NASDAQ-100", "index": 4, "country": "United States"},
    "FTSE 100": {"link": "https://en.wikipedia.org/wiki/FTSE_100_Index", "index": 4, "country": "United Kingdom"},
    "DAX": {"link": "https://en.wikipedia.org/wiki/DAX", "index": 4, "country": "Germany"},
    "CAC 40": {"link": "https://en.wikipedia.org/wiki/CAC_40", "index": 4, "country": "France"},
    "Hang Seng Index": {"link": "https://en.wikipedia.org/wiki/Hang_Seng_Index", "index": 6, "country": "Hong Kong"},
    "ASX 200": {"link": "https://en.wikipedia.org/wiki/S%26P/ASX_200", "index": 2, "country": "Australia"},
    "S&P/TSX Composite Index": {"link": "https://en.wikipedia.org/wiki/S%26P/TSX_Composite_Index", "index": 3, "country": "Canada"}
    
}

#saving as a json
files = "index_links.json"
with open(files, "w") as file:
    #convert to json type
    json_dict = json.dumps(urls)
    #Saving file
    json.dump(json_dict, file)
    
# Download components lists from S&P 500 from wikipedia
def getting_indexes(index: str = "S&P 500", file: str="index_links.json") -> pd.DataFrame:
    """
    SUMMARY.

    This method downloads all assets from each index.

    Parameters
    ----------
    index : str, optional
        Index that will be downloaded.
        The default is "S&P 500".
        
    file : str, optional
        JSON file containing the URLs and table indexes.
        The default is "index_links.json".

    Returns
    -------
    pd.DataFrame
        DataFrame containing the components of the selected index.
    """
    
    #load document
    urls_document = json.load(open(file, "r"))
    urls_dict = json.loads(urls_document) # converts data to a dictionary
    
    #Make sure than the index it's available
    assert index in list(urls_dict.keys()), f"The value must to be one of the nexts {list(urls_dict.keys())}"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(urls_dict[index]["link"], headers=headers)
    tables_assets = pd.read_html(StringIO(response.text))
    
    components = tables_assets[urls_dict[index]["index"]]
    
    return components


# Example (Reminder)
if __name__ == "__main__":
    
    # Definir índice
    ticker = "S&P 500"
    file = "index_links.json"
    
    # Obtener activos
    components = getting_indexes(ticker, file)
    print(components)