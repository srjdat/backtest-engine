from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC): 
    @abstractmethod
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def generate_signal(self, df: pd.DataFrame) -> str: 
        return ""