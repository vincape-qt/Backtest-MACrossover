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

    df['Signal'] = 0

    # Crossover up --> buy
    df.loc[(df['Diff'].shift(1) <= 0) & (df['Diff'] > 0), 'Signal'] = 1

    # Crossover down --> sell
    df.loc[(df['Diff'].shift(1) >= 0) & (df['Diff'] < 0), 'Signal'] = -1
    # Making order one day after bc we work on close price
    positions = []
    for signal in df['Signal'].shift(-1) :
        position = 0 
        if signal == 1 :
            position = 1
        positions.append(position)
    df['Position'] = positions

    #calcul of every trade's return
    return_on_trade = []
    position_open = False
    buy_price = 0
    sell_price = 0
    
    for index, row in df.iterrows():
        signal = row['Signal']

        if signal == 1 and not position_open:
            buy_price = row['Close']
            position_open = True

        elif signal == -1 and position_open:
            sell_price = row['Close']
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

    






