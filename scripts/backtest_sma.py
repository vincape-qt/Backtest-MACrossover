import numpy as np
import pandas as pd
import yfinance as yf

from scripts.clean_data import get_clean_data

def backtest_sma(short, long) :
    df = get_clean_data('SPY','2022-01-01','2025-05-31')

    #define the short and long moving averages
    df['MA_short'] = df['Close'].rolling(window=short).mean()
    df['MA_long'] = df['Close'].rolling(window=long).mean()

    #generate the trading signal to buy
    df['Diff'] = df['MA_short'] - df['MA_long']
    df['Signal'] = 0
    df['Signal'] = np.where(
    (df['Diff'].shift(1) <= 0) & (df['Diff'] > 0), 1,  # crossover up --> buy
    )
    df['Signal'] = np.where(
        (df['Diff'].shift(1) >= 0) & (df['Diff'] < 0), -1,  # crossover down --> sell
        df['Signal']
    )

    #making order one day after bc we work on close price
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
    
    for i in range(len(df)):
        row = df.iloc[i]

        if row['Signal'] == 1 and not position_open:
            buy_price = row['Close']
            position_open = True

        elif row['Signal'] == -1 and position_open:
            sell_price = row['Close']
            position_open = False

            return_on_trade.append(sell_price - buy_price)
    
    mean_return = return_on_trade.mean()

    






