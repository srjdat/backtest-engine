import datetime
import yfinance as yf
import pandas as pd
import numpy as np
from engine import Engine
from portfolio import Portfolio

# import all the strategies
from strategy.mystrategy import MyStrategy
from strategy.sma_crossover import SMA_Crossover


ticker = 'AAPL'
start_date = '2013-08-28'
end_date = '2026-06-14'

# start from a year back so we can have 52 week high low and other stuff already loaded in
start_date_original = datetime.date.strptime(start_date, "%Y-%m-%d")
start_date = start_date_original.replace(year=start_date_original.year-1)
df = pd.DataFrame(yf.Ticker(ticker=ticker).history(start=start_date, end=end_date))

df["pos"] = np.arange(len(df)) 

# all these calculations are from https://github.com/srjdat/finance-trader
df['52wkHigh'] = df.High.rolling(window=252).max()
df['52wkLow'] = df.Low.rolling(window=252).min()
df['Distance From High'] = (df.Close - df['52wkHigh']) / df['52wkHigh'] * 100
df['Distance From Low'] = (df.Close - df['52wkLow']) / df['52wkLow'] * 100

# moving average
df["SMA20"] = df.Close.rolling(window=20).mean()
df["SMA50"] = df.Close.rolling(window=50).mean()

# bollinger bands
df['Upper Band'] = 2 * df.Close.rolling(window=20).std() + df['SMA20']
df['Lower Band'] = df['SMA20'] - 2 * df.Close.rolling(window=20).std()

# average true range
# tr = max(high, close_prev) - min(low, close_prev)
close_prev = df['Close'].shift(1)
tr1 = pd.concat([df['High'], close_prev], axis=1).max(axis=1)
tr2 = pd.concat([df['Low'], close_prev], axis=1).min(axis=1)
true_range = tr1 - tr2

n = 14
# instantiate the atr dataframe
temp = true_range.iloc[0:n].mean() # get the first 14 day average

# start the atr series
atr_values = [np.nan] * (n-1) # first 14 is going to be nan
atr_values.append(temp) # add temp to the 14th index

# get the rest
for i in range(n, len(true_range)): # smma
    temp = (temp * (n-1) + true_range.iloc[i]) / n  # yesterday's temp value becomes today's atr value
    atr_values.append(temp)  # add today's temp into atr

df['ATR'] = pd.Series(data=atr_values, index=true_range.index) # add it into df

# find the volatility
df["Daily Change"] = df["Close"].pct_change()
df["Volatility"] = 100 * (df["Daily Change"].rolling(window=20).std())

# RVOL
# find sma 10 for volume
df['Volume SMA 20'] = df['Volume'].rolling(window=20).mean()
df['rvol'] = df.Volume/df['Volume SMA 20'].shift(1)

# find rsi
daily_change = df["Close"].diff()  # today - yesterday

# change up and down
change_up, change_down = daily_change.copy(), daily_change.copy()
change_up[change_up < 0] = 0  # up = close_now - close_prev down = 0
change_down[change_down > 0] = 0  # up = 0 down = close_prev - close_now

# average up and down
average_up = change_up.rolling(14).mean()  # get average for up
average_down = change_down.rolling(14).mean().abs() #  get average for down
df['rsi'] = 100 * average_up / (average_up + average_down)
# these are the most widely used values (got this from charles schwab youtube video: https://youtu.be/hbcCykbX14U?si=eaaSyrdYvQqW3a8Q)
oversold = np.full(len(df), 30)  # 1d array with 30 as all the values
overbought = np.full(len(df), 70)  # 1d array with 70 as all the values

# MACD
# ema
df["EMA12"] = df.Close.ewm(span=12).mean()
df["EMA26"] = df.Close.ewm(span=26).mean()
df["MACD"] = df["EMA12"] - df["EMA26"]
df["Signal Line"] = df["MACD"].ewm(span=9).mean()
df["macd hist"] = df["MACD"] - df["Signal Line"]

# make a new column with tomorrow's open for trades
df['Tomorrow Open'] = df['Open'].shift(-1)

# returns over windows
df['one_day_window'] = (df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1) * 100
df['one_week_window'] = (df['Close'] - df['Close'].shift(5)) / df['Close'].shift(5) * 100
df['one_month_window'] = (df['Close'] - df['Close'].shift(21)) / df['Close'].shift(21) * 100
df['three_month_window'] = (df['Close'] - df['Close'].shift(63)) / df['Close'].shift(63) * 100
df['six_month_window'] = (df['Close'] - df['Close'].shift(125)) / df['Close'].shift(125) * 100
df['one_year_window'] = (df['Close'] - df['Close'].shift(252)) / df['Close'].shift(252) * 100

# make df only from start date to end date
df = df.iloc[250:len(df)]

s1 = SMA_Crossover()
p1 = Portfolio(15000)
e1 = Engine(df=df, strategy=s1, portfolio=p1)
e1.run()