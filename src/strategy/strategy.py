from abc import ABC, abstractmethod
import pandas as pd
from portfolio import Portfolio

class Strategy(ABC): 
    @abstractmethod
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def generate_signal(self, df: pd.DataFrame) -> str: 
        return ""
    
    @abstractmethod 
    def generate_buy_shares(self, df: pd.DataFrame, portfolio: Portfolio, stock_price: float) -> int: 
        return 0
    
    @abstractmethod
    def generate_sell_shares(self, df: pd.DataFrame, portfolio: Portfolio, stock_price: float) -> int: 
        # return 80 percent of all the shares you have
        shares = int(portfolio.total_shares * .8)

        return shares