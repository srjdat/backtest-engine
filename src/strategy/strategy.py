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
    def generate_shares(self, df: pd.DataFrame, portfolio: Portfolio, stock_price: float) -> int: 
        return 0