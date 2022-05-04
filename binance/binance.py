import ccxt, yfinance
import pandas_ta as ta
import pandas as pd
# import config
import requests
from dotenv import load_dotenv
import os

load_dotenv()

BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')



exchange_id = 'binanceus'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    "apiKey": BINANCE_API_KEY,
    "secret": BINANCE_SECRET_KEY
})

webhook = os.getenv('DISCORD_WEBHOOK')


bars = exchange.fetch_ohlcv('ETH/USDT', timeframe='5m', limit=500)


df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
adx = df.ta.adx()
macd = df.ta.macd()
rsi = df.ta.rsi()

df = pd.concat([df, adx, macd, rsi], axis=1)

print(df)

# last_row = df.iloc[-1]
# print(last_row)

# if last_row['ADX_14'] >= 25:
#     if last_row["DMP_14"] > last_row['DMN_14']:
#         message = f"STRONG UPTREND: The ADX is {last_row['ADX_14']:.2f}"
#     if last_row["DMN_14"] > last_row['DMP_14']:
#         message = f"STRONG DOWNTEND: The ADX is {last_row['ADX_14']:.2f}" 
#         payload = {
#         'username': "Donkey Bot",
#         "content": message
#     }
    
#     requests.post(webhook, json=payload)

# if last_row['ADX_14'] < 25:
#     message = f"NO TREND: The ADX is {last_row['ADX_14']:.2f}"
#     print(message)
    
#     payload = {
#         'username': "Donkey Bot",
#         "content": message
#     }
    
#     requests.post(webhook, json=payload)