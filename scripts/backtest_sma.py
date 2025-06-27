import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


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

    #generate the trading signal to buy or sell
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

    # Making order one day after because we work on close price
    positions = [0]
    for i in range(1,len(df['Signal'])) :
        position = 0 
        if series_signal[i-1] == 1 :
            position = 1
        positions.append(position)
    df['Position'] = positions

    # Calculation of every trade's return
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


def plot_backtest(short, long):
    trade, df = backtest_sma(short, long)
    df_close = df['Close']
    signals = [df['Signal'].iloc[i] for i in range(len(df))]
    plt.figure(figsize=(15, 6))
    plt.plot(df.index, df_close['SPY'], label='Prix de clôture SPY', color='black', linewidth=1)
    plt.plot(df.index, df['MA_short'], label='MA 8 jours', color='blue', linestyle='--')
    plt.plot(df.index, df['MA_long'], label='MA 21 jours', color='red', linestyle='--')

    # # Purchase points
    # buy_signals = [elt for elt in signals if elt == 1]
    # plt.scatter(df.index, buy_signals, marker='^', color='green', label='Achat', s=100)

    # # Sale points
    # sell_signals = [elt for elt in signals if elt == -1]
    # plt.scatter(df.index, sell_signals, marker='v', color='red', label='Vente', s=100)

    plt.title('Backtest stratégie MA crossover')
    plt.xlabel('Date')
    plt.ylabel('Prix')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_backtest(8,21)

    






