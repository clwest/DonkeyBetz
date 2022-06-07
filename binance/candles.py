import ccxt, yfinance
import pandas_ta as ta
import pandas as pd
# import config
import requests
from dotenv import load_dotenv
import os

load_dotenv()


load_dotenv()

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')



exchange_id = 'binanceus'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    "apiKey": BINANCE_API_KEY,
    "secret": BINANCE_SECRET_KEY
})
print(exchange)




# # Get all candle patterns (This is the default behaviour)
# df = df.ta.cdl_pattern(name="all")

# # Get only one pattern
# df = df.ta.cdl_pattern(name="doji")

# # Get some patterns
# df = df.ta.cdl_pattern(name=["doji", "inside"])