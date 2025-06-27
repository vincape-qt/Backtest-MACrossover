# project-backtest
Build a backtest model based on the elementary strategy of the Crossover Moving Average applied to an ETF or a large index (SP500, Nasdaq, BTC/USD).

The strategy consists in having two averages of the closing values of our financial asset, one long (21 days) which allows us to see the asset's movement on a large scale of time, the other short (8 days) which highlights the short-term trends of our asset's movement.
Therefore, we will buy when the short average goes above the long one (when MA_8 > MA_21) because we enter in a positive period, and we sell when the short average goes below the long one to avoid the less successful periods.

The project is composed in different parts, one data (which ignores git), to print the processed data; one scripts with the backtesting code which returns the graph of the backtesting, with three curves (closing price of the asset, short average, long average); one venv which allows to import libraries more smoothly, a requirements.txt which lists all the libraries' versions.

Libraries used : matplotlib.pyplot, yfinance, pandas, numpy

Disclaimer : this project is only for educational purposes, it doesn't represent an investment advice. Never trade without a real, efficient and approved strategy.

Vincent Capellano - Student at ISAE-SUPAERO, passionate about quantitative finance
