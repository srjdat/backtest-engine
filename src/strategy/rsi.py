from pandas import DataFrame
import math
from portfolio import Portfolio
from strategy.strategy import Strategy

class RSI(Strategy): 
    def __init__(self) -> None:
        super().__init__()

    def generate_signal(self, df: DataFrame) -> str:
        if df['rsi'].iloc[-1] < 30: # over sold = buy signal
            return "buy"
        elif df['rsi'].iloc[-1] > 70: # over bought = sell signal
            return "sell"
        else: 
            return "hold"

    def generate_buy_shares(self, df: DataFrame, portfolio: Portfolio, stock_price: float) -> int:
        cash: float = portfolio.cash

        # only buy 80% of what you can afford
        shares = math.floor((cash * .8) / stock_price) # round it down because maybe one more share will be too much
        # we are rounding it down here, but if something still goes wrong it's fine because the buy method checks if we are buying more than we can afford

        return shares
    
    def generate_sell_shares(self, df: DataFrame, portfolio: Portfolio, stock_price: float) -> int:
        return super().generate_sell_shares(df, portfolio, stock_price)