import pandas as pd
from portfolio import Portfolio
from strategy import Strategy
import numpy as np

class Engine: 
    df: pd.DataFrame
    portfolio: Portfolio
    trade_log: list
    pnl_list: list
    data_so_far: pd.DataFrame

    def __init__(self, df: pd.DataFrame, strategy: Strategy, portfolio: Portfolio) -> None:
        self.df = df
        self.strategy = strategy
        self.portfolio = portfolio
        self.trade_log = []
        self.pnl_list = []

    def run(self): 
        for index, row in self.df.iterrows(): 
            # have to call mark to market every day
            self.portfolio.mark_to_market(current_price=row['Close'], pos=row['pos'])

            # add onto data so far 
            self.data_so_far = self.df[0: (int)(row['pos'] + 1)] # have to turn row['pos'] + 1 into an int because it is a float here
            self.data_so_far = self.data_so_far.drop('Tomorrow Open', axis=1)

            # call the strategy to receive the signal
            signal = self.strategy.generate_signal(self.data_so_far)
            if signal == "buy" and self.portfolio.shares == 0: 
                # we send up until today's close price to get a signal and if it's a buy signal we buy when the market opens tomorrow hence row['Open']
                if not pd.isna(row['Tomorrow Open']):
                    entry_price = row['Tomorrow Open'] # get tomorrow's open to buy
                    shares = 10 # currently 10 only, will change it later 
                    self.portfolio.buy(entry_price=entry_price, shares=shares) 
                    self.trade_log.append((entry_price, shares, "buy", row['pos'])) # add to log as buy
                else:
                    pass
            elif signal == "sell" and self.portfolio.shares > 0: 
                # today after the market closes we get a signal based on everything so far. so when we eventually sell it's going to be tomorrow's open price that we sell at
                if not pd.isna(row['Tomorrow Open']): 
                    exit_price = row['Tomorrow Open'] # get tomorrow open to sell it at
                    self.trade_log.append((exit_price, self.portfolio.shares, "sell", row['pos'])) # add to log as sell
                    pnl = self.portfolio.sell(exit_price=exit_price)
                    self.pnl_list.append((pnl, row['pos']))
                else: 
                    pass

        # at the end of the run function call the output function which will output all the things 
        self.output()
    
    def output(self): 
        np.set_printoptions(legacy='1.25')

        print("equity curve")
        for item in self.portfolio.equity_curve: 
            print(item)
        print("trade log")
        for item in self.trade_log: 
            print(item)
        print(f"cash {self.portfolio.cash}")
        print(f"equity {self.portfolio.equity}")
        print(f"shares {self.portfolio.shares}")
        print(f"pnl {self.portfolio.pnl}")