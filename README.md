## Backtesting Engine
This is the second part to finance-trader (my other project). This project allows the user to test strategies they have developed or are testing. There is a base strategy class which is used to return a "buy", "sell", or "hold" signal alongside how many shares to buy or sell.

### How to run
1. Clone the repo and create a virtual environment using `python3 -m venv venv` then `source venv/bin/activate`
2. Run `pip install -r requirements.txt` to install all requirements. 
3. Run `python src/main.py` to run the program

### Output
Outputs a PNL list, Trade Log, total cash, equity, shares, and final PNL.   
You can change what company you want to test on in main.py by changing `ticker = 'AAPL'` to whatever company's ticker you want.    
If you want to change the strategy you can do so by changing `s1 = SMA_Crossover()` to `s1 = MyStrategy() or RSI()`. 

### Additional Information
I will add more strategies later as I learn more about trading and finance in general.   
**Do not use this program as a way to trade. This isn't perfect and will make mistakes. Please do research before trading!!**