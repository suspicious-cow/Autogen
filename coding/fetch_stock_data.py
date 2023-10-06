# filename: fetch_stock_data.py

# Import required libraries
import yfinance as yf
import pandas as pd
from datetime import datetime

# Define the stock symbols
stock_symbols = ['NVDA', 'TSLA']

# Define the date range (YTD)
start_date = datetime(datetime.now().year, 1, 1)
end_date = datetime.now()

# Fetch the stock market data
stock_data = yf.download(stock_symbols, start=start_date, end=end_date)

# Keep only the adjusted close prices
stock_data = stock_data['Adj Close']

# Print the fetched stock data
print(stock_data)