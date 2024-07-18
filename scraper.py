import yfinance as yf
import pandas as pd

# Define the indexes and their corresponding Yahoo Finance tickers
indexes = {
    'S&P 500': '^GSPC',
    'Dow Jones Industrial Average': '^DJI',
    'NASDAQ Composite': '^IXIC',
    'FTSE 100': '^FTSE',
    'DAX': '^GDAXI',
    'CAC 40': '^FCHI',
    'Nikkei 225': '^N225',
    'SSE Composite Index': '000001.SS',
    'Hang Seng Index': '^HSI',
    'KOSPI': '^KS11',
    'Nifty 50': '^NSEI',
    'ASX 200': '^AXJO',
    'Bovespa': '^BVSP'
}

# Define the period and interval for the data
period = 'max'  # You can also specify a range like '5y', '1y', etc.
interval = '1mo'  # Monthly data; use '1d' for daily data

# Function to download and save data for each index
def download_data(index_name, ticker):
    data = yf.download(ticker, period=period, interval=interval)
    data.reset_index(inplace=True)
    data.to_csv(f'{index_name.replace(" ", "_")}.csv', index=False)
    print(f"Data for {index_name} saved to {index_name.replace(' ', '_')}.csv")

# Loop through each index and download its data
for index_name, ticker in indexes.items():
    download_data(index_name, ticker)

