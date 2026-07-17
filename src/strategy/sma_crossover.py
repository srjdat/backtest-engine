from pandas import DataFrame
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