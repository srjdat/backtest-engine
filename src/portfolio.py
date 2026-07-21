import math

class Portfolio: 
    cash: float
    equity: float
    shares: list
    total_shares: int
    pnl: float
    equity_curve: list

    def __init__(self, cash) -> None:
        self.cash = cash
        self.equity = cash
        self.shares = []
        self.pnl = 0
        self.equity_curve = []
        self.total_shares = 0

    def buy(self, entry_price, user_shares) -> int: 
        # final check before getting added to shares
        # shares is a list so i add 
        if entry_price * user_shares > self.cash: 
            user_shares = math.floor(self.cash / entry_price) # change shares to how much we can afford
            self.shares.append((user_shares, entry_price)) # add it to our share list
            self.total_shares += user_shares # add it to the total count
        else: 
            self.shares.append((user_shares, entry_price))  # otherwise if we can afford add it to share list
            self.total_shares += user_shares

        # calculate how much cash you lose 
        self.cash -= (user_shares * entry_price) 

        return user_shares # returns the shares that we bought depending on if we changed it or not

    def sell(self, exit_price: float, user_shares) -> float: 

        self.total_shares -= user_shares # decrease the total shares you hold
        cash_gained = (exit_price * user_shares) # how much cash we gained
        self.cash += cash_gained # cash += how much you sell
        trade_pnl = cash_gained # how much profit or loss you made this sell 
        
        new_share_list = []
        # loop through all the shares bought
        for item in self.shares: 
            if user_shares != 0: # we still have shares to sell
                diff = user_shares - item[0] # difference between shares we want to sell and the first set of shares we bought/have
                if diff <= 0: # if the first set is shares is the same as the number of shares we want to sell or if it's more 
                    if diff < 0: # we have left over shares
                        new_share_list.append((item[0] - user_shares, item[1])) # we have left over shares in this element which we add to the new list
                        trade_pnl -= (user_shares * item[1]) # deduct shares we sold * entry price
                    else: # diff is equal to zero meaning we sold all the shares in this element
                        # we don't have to add anything to the new list
                        trade_pnl -= (item[0] * item[1])
                    user_shares = 0 # we sold all the shares we wanted to sell 
                else: # we have more shares to sell 
                    # we don't add this element to the new list
                    user_shares = diff # share is the old share - item[0]
                    trade_pnl -= (item[0] * item[1]) # subtract the number of shares times the entry price from the cash gained
            else: # we have no more shares to sell shares == 0
                new_share_list.append((item[0], item[1])) # append this to the new list   
                    
        self.pnl += trade_pnl # add new pnl to existing pnl
        
        self.shares = new_share_list

        return trade_pnl
    
    def mark_to_market(self, current_price, pos): 

        share_current_price = 0 # var to calculate shares * current price
        for item in self.shares: 
            share_current_price += item[0] * current_price
        
        self.equity = self.cash + share_current_price # equity = cash + current prices of all stocks

        self.equity_curve.append((pos, self.equity))
