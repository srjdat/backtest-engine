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

    def buy(self, entry_price, shares): 
        self.entry_price = entry_price

        # check if we bought more than we can afford
        if entry_price * shares > self.cash: 
            self.shares = math.floor(self.cash / entry_price)
        else: 
            self.shares = shares

        # calculate how much cash you lose 
        self.cash -= (self.shares * self.entry_price)

    def sell(self, exit_price: float) -> float: 
        self.cash += (exit_price * self.shares) 
        trade_pnl = (self.shares * exit_price) - (self.shares * self.entry_price) # type: ignore
        self.pnl += trade_pnl
        self.entry_price = None
        self.shares = 0

        return trade_pnl
    
    def mark_to_market(self, current_price, pos): 
        self.equity = self.cash + (self.shares * current_price) # recalculate equity every day
        self.equity_curve.append((pos, self.equity))
        print(f"cash: {self.cash} equity {self.equity} \nequity curve {self.equity_curve}")