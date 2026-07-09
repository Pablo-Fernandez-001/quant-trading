"""
original code example:
    # -*- coding: utf-8 -*-
# Importar librerías
import pandas_datareader as pdr # pip install pandas-datareader
import pandas_datareader.data as web
from datetime import datetime 
import matplotlib.pyplot as plt


# Obtener datos históricos
fecha_inicio = "2020-01-01"
fecha_final = "2024-01-01"
ticker = "AMZN"

# Fuente: Stooq
try:
    df = pdr.get_data_stooq(symbols=ticker, start=fecha_inicio, end=fecha_final)
    df = df[::-1]
    print(df)
except Exception as error:
    print("No se pudo recuperar la información con error ->", error)
    

# Fuente: Stooq
try:
    df = pdr.stooq.StooqDailyReader(symbols=ticker, start=fecha_inicio, end=fecha_final).read()
    df = df[::-1]
    print(df)
except Exception as error:
    print("No se pudo recuperar la información con error ->", error)
    
    
# Fuente: Yahoo
try:
    df = pdr.get_data_yahoo(symbols=ticker, start=fecha_inicio, end=fecha_final)
    df = df[::-1]
    print(df)
except Exception as error:
    print("No se pudo recuperar la información con error ->", error)
    

# Descargar múltiples tickers
tickers = ["AMZN", "AAPL", "MSFT"]
fecha_inicio = datetime(2020, 1, 1)
fecha_final = datetime(2024, 1, 1)
df = web.DataReader(name=tickers, data_source="stooq", start=fecha_inicio, end=fecha_final)
    
    
close = df["Close"]
    
    
# Graficar
close.plot(figsize=(22, 12))
plt.title("Precios de Cierre", size=25)
plt.xlabel("Fecha", size=20)
plt.ylabel("Precios", size=20)
plt.legend()
plt.show()
    
    
# Recordatorio:
#   - Debemos de mantener actualizadas las librerías para evitar cualquier posible error (pip install --upgrade pandas-datareader)

"""

# -*- coding: utf-8 -*-
# Import libraries
import types
import pandas as pd
import pandas_datareader as pdr  # pip install pandas-datareader
import pandas_datareader.data as web
from datetime import datetime
import matplotlib.pyplot as plt


# ============================
# Local patch for old examples
# ============================

_original_DataReader = web.DataReader


def _download_yahoo(symbols=None, start=None, end=None):
    import yfinance as yf

    if isinstance(symbols, (list, tuple)):
        yahoo_symbols = [
            str(symbol).replace(".US", "").replace(".us", "").upper()
            for symbol in symbols
        ]
    else:
        yahoo_symbols = str(symbols).replace(".US", "").replace(".us", "").upper()

    df = yf.download(
        yahoo_symbols,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
        group_by="column",
        threads=False
    )

    if df.empty:
        raise ValueError(f"Could not retrieve data for {symbols}")

    return df


def get_data_stooq(symbols=None, start=None, end=None, *args, **kwargs):
    """
    Try to use Stooq.
    If Stooq fails, use yfinance as a fallback.
    """
    try:
        def read_one_stooq_symbol(symbol):
            symbol = str(symbol).lower()

            if "." not in symbol:
                symbol = symbol + ".us"

            start_date = pd.to_datetime(start).strftime("%Y%m%d")
            end_date = pd.to_datetime(end).strftime("%Y%m%d")

            url = f"https://stooq.com/q/d/l/?s={symbol}&d1={start_date}&d2={end_date}&i=d"

            df = pd.read_csv(url)

            if df.empty or "Date" not in df.columns:
                raise ValueError("Stooq did not return valid data")

            df["Date"] = pd.to_datetime(df["Date"])
            df = df.set_index("Date")

            return df

        if isinstance(symbols, (list, tuple)):
            data = {}

            for symbol in symbols:
                data[symbol] = read_one_stooq_symbol(symbol)

            df = pd.concat(data, axis=1)

            # Convert columns from:
            # AMZN -> Close
            # to:
            # Close -> AMZN
            df = df.swaplevel(0, 1, axis=1).sort_index(axis=1)

            return df

        return read_one_stooq_symbol(symbols)

    except Exception:
        return _download_yahoo(symbols=symbols, start=start, end=end)


def get_data_yahoo(symbols=None, start=None, end=None, *args, **kwargs):
    return _download_yahoo(symbols=symbols, start=start, end=end)


class StooqDailyReader:
    def __init__(self, symbols=None, start=None, end=None, *args, **kwargs):
        self.symbols = symbols
        self.start = start
        self.end = end

    def read(self):
        return get_data_stooq(
            symbols=self.symbols,
            start=self.start,
            end=self.end
        )


def DataReader(name=None, data_source=None, start=None, end=None, *args, **kwargs):
    if str(data_source).lower() == "stooq":
        return get_data_stooq(symbols=name, start=start, end=end)

    if str(data_source).lower() == "yahoo":
        return get_data_yahoo(symbols=name, start=start, end=end)

    return _original_DataReader(
        name=name,
        data_source=data_source,
        start=start,
        end=end,
        *args,
        **kwargs
    )


# Apply local patch
pdr.get_data_stooq = get_data_stooq
pdr.get_data_yahoo = get_data_yahoo
pdr.stooq = types.SimpleNamespace(StooqDailyReader=StooqDailyReader)
web.DataReader = DataReader


# ============================
# Original example code
# ============================

# Get historical data
start_date = "2020-01-01"
end_date = "2024-01-01"
ticker = "AMZN"

# Source: Stooq
try:
    df = pdr.get_data_stooq(symbols=ticker, start=start_date, end=end_date)
    df = df[::-1]
    print(df)

except Exception as error:
    print("We can't recover all the information with the error ->", error)


# Source: Stooq
try:
    df = pdr.stooq.StooqDailyReader(
        symbols=ticker,
        start=start_date,
        end=end_date
    ).read()

    df = df[::-1]
    print(df)

except Exception as error:
    print("We can't recover all the information with the error ->", error)


# Source: Yahoo
try:
    df = pdr.get_data_yahoo(symbols=ticker, start=start_date, end=end_date)
    df = df[::-1]
    print(df)

except Exception as error:
    print("We can't recover all the information with the error ->", error)


# Download multiple tickers
tickers = ["AMZN", "AAPL", "MSFT"]
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 1, 1)

df = web.DataReader(
    name=tickers,
    data_source="stooq",
    start=start_date,
    end=end_date
)


close = df["Close"]


# Plot
close.plot(figsize=(22, 12))
plt.title("Close Prices", size=25)
plt.xlabel("Date", size=20)
plt.ylabel("Prices", size=20)
plt.legend()
plt.show()