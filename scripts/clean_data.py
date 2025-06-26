import yfinance as yf
import pandas as pd

def get_clean_data(ticker, start_date, end_date) :
    df = yf.download(tickers = ticker,start = start_date,end = end_date)
    #Keep the columns 'Close' and 'Date'
    df = df[['Close']]
    df = df.dropna()
    return df