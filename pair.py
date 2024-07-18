import yfinance as yf
import pandas as pd
from datetime import datetime

# Define currency pairs and their Yahoo Finance symbols
currency_pairs = {
    'EUR/USD': 'EURUSD=X',
    'GBP/USD': 'GBPUSD=X',
    'USD/JPY': 'JPY=X',
    'AUD/USD': 'AUDUSD=X',
    'USD/CAD': 'CAD=X',
    'USD/CHF': 'CHF=X',
    'CNY/USD': 'CNY=X'
}

# Function to fetch and save currency pair data
def fetch_currency_data(pair_name, symbol):
    # Fetch data
    data = yf.download(symbol, interval='1mo', period='max')

    # Save to CSV
    filename = f'{pair_name.replace("/", "_")}_1mo.csv'
    data.to_csv(filename)
    print(f'Saved data for {pair_name} to {filename}')

# Fetch data for all currency pairs
for pair_name, symbol in currency_pairs.items():
    fetch_currency_data(pair_name, symbol)
