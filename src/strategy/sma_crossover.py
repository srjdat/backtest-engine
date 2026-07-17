from pandas import DataFrame
import math
from portfolio import Portfolio
from strategy.strategy import Strategy

class SMA_Crossover(Strategy):
    def __init__(self) -> None:
        super().__init__()

    def generate_signal(self, df: DataFrame) -> str:
        crossover: int = 0
        if (df['SMA20'].iloc[-2] < df['SMA50'].iloc[-2] and df['SMA20'].iloc[-1] > df['SMA50'].iloc[-1]):
            crossover = 1
        elif  (df['SMA20'].iloc[-2] > df['SMA50'].iloc[-2] and df['SMA20'].iloc[-1] < df['SMA50'].iloc[-1]):
            crossover = -1

        if crossover == 0: 
            return "hold"
        elif crossover == 1: 
            return "buy"
        elif crossover == -1: 
            return "sell"
        

    def generate_shares(self, df: DataFrame, portfolio: Portfolio, stock_price: float) -> int:
        cash: float = portfolio.cash

        # only buy 80% of what you can afford
        shares = math.floor((cash * .8) / stock_price) # round it down because maybe one more share will be too much
        # we are rounding it down here, but if something still goes wrong it's fine because the buy method checks if we are buying more than we can afford

        return shares