import math

class Portfolio: 
    cash: float
    equity: float
    shares: int
    pnl: float
    equity_curve: list

    def __init__(self, cash) -> None:
        self.cash = cash
        self.equity = cash
        self.shares = 0
        self.entry_price = None
        self.pnl = 0
        self.equity_curve = []

    def buy(self, entry_price, shares) -> int: 
        self.entry_price = entry_price

        # check if we bought more than we can afford
        if entry_price * shares > self.cash: 
            shares = math.floor(self.cash / entry_price) # change shares to how much we can afford
            self.shares += shares # add it to our share count
        else: 
            self.shares += shares # otherwise if we can afford add it to share count

        # calculate how much cash you lose 
        self.cash -= (shares * entry_price) 

        return shares # returns the shares that we bought depending on if we changed it or not

    def sell(self, exit_price: float, shares) -> float: 
        self.cash += (exit_price * shares) 
        trade_pnl = (shares * exit_price) - (shares * self.entry_price) # type: ignore
        self.pnl += trade_pnl
        self.shares -= shares
        if self.shares == 0: # do this after shares have been subtracted to see if all shares are sold or not
            self.entry_price = None

        return trade_pnl
    
    def mark_to_market(self, current_price, pos): 
        self.equity = self.cash + (self.shares * current_price) # recalculate equity every day
        self.equity_curve.append((pos, self.equity))

    def get_shares(self) -> int: 
        return self.shares
    
    def get_cash(self) -> float: 
        return self.cash