import numpy as np
import pandas as pd
import yfinance as yf


def get_clean_data(ticker, start_date, end_date) :
    df = yf.download(tickers = ticker,start = start_date,end = end_date)
    df = df[['Close']]
    df = df.dropna(how= 'any') #every row with a NaN is deleted   
    return df


def backtest_sma(short, long) :
    df = get_clean_data('SPY','2022-01-01','2025-05-31')

    #define the short and long moving averages
    df['MA_short'] = df['Close'].rolling(window=short).mean()
    df['MA_long'] = df['Close'].rolling(window=long).mean()

    #generate the trading signal to buy
    df['Diff'] = df['MA_short'] - df['MA_long']

    series_signal = [0]
    series_diff = df['Diff']

    for i in range(1,len(series_diff)) :
        if series_diff.iloc[i-1] < 0 and series_diff.iloc[i] > 0 :
            series_signal.append(1)
        elif series_diff.iloc[i-1] > 0 and series_diff.iloc[i] < 0 :
            series_signal.append(-1)
        else :
            series_signal.append(0)
    
    df['Signal'] = series_signal

    # Making order one day after bc we work on close price
    positions = [0]
    for i in range(1,len(df['Signal'])) :
        position = 0 
        if series_signal[i-1] == 1 :
            position = 1
        positions.append(position)
    df['Position'] = positions

    #calcul of every trade's return
    return_on_trade = []
    position_open = False
    buy_price = 0
    sell_price = 0
    df_close = df['Close'] # We define new variables to simplify the data's recuperation
    series_close = df_close['SPY']

    for i in range(len(series_close)) :
        if series_signal[i] == 1 and not position_open :
            buy_price = series_close.iloc[i]
            position_open = True

        elif series_signal[i] == -1 and position_open :
            sell_price = series_close.iloc[i]
            position_open = False
            return_on_trade.append(sell_price - buy_price)
    
    trade = {"gain" : 0, "loss" : 0}
    gain = 0
    loss = 0
    for elt in return_on_trade :
        if elt > 0 :
            gain += elt
        else :
            loss += elt
    trade['gain'] = gain
    trade['loss'] = loss

    return trade, df

print(backtest_sma(8, 21))

    






