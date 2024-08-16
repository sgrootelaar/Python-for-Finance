## TRADING STRATEGY BACKTESTING - Classes 
## SAM GROOTELAAR 
## 10-08-2024


#%% Dependencies
import numpy as np 
import pandas as pd 
import yfinance as yf

#%% Define Results Class 

#%% Define Broad Trading Strategy Class 
class trading_strategy(): 
    def __init__(self, name, trading_rule): 
        self.name = name # name of strategy 
        self.trading_rule = trading_rule # brief description of the strategy  
        
#%% Simple Moving Average Trading Strategy
class SMA(trading_strategy):
    
    def __init__(self, symbol, ma_var_1, ma_var_2, start, end = None):
        name = "SMA"
        trading_rule = "Long if short window MA is greater than long window MA and vice versa."
        super().__init__(name, trading_rule) 
        
        self.symbol = symbol
        self.ma_var_1 = ma_var_1
        self.ma_var_2 = ma_var_2
        self.start = start 
        self.end = end
        self.init_data()

    def init_data(self): 
        # Pulls data from Yahoo Finance and calculates key variables
        
        # Download Data from Yahoo Finance
        self.data = yf.download(self.symbol, start = self.start, end = self.end).Close.to_frame()
            
        # Calculate Key Series
        self.data["log_return"] = np.log(self.data.Close.div(self.data.Close.shift(1)))
        self.data["SMA{}".format(self.ma_var_1)] = self.data.Close.rolling(window = self.ma_var_1).mean()
        self.data["SMA{}".format(self.ma_var_2)] = self.data.Close.rolling(window = self.ma_var_2).mean()

    def run(self, display = True):
        # Runs the backtest and calculates the key performance metrics
        temp = self.data.copy() # create a copy of the dataframe without NAs

        ### Calculate Trading Position ---------------------------------------------------------------------------- 
        temp["position"] = np.where(temp["SMA{}".format(self.ma_var_1)]> temp["SMA{}".format(self.ma_var_2)],1,-1)

        ### Calculate Resulting Return Profile -------------------------------------------------------------------- 
        temp["log_strategy_return"] = temp["log_return"] * temp.position.shift(1)
        temp["log_cumm_return"] = temp["log_return"].cumsum().apply(np.exp)
        temp["log_strategy_cumm_return"] = temp["log_strategy_return"].cumsum().apply(np.exp)
        self.results = temp.dropna()

        ### Calculate Performance Metrics -------------------------------------------------------------------------
        self.performance = self.results["log_strategy_cumm_return"].iloc[-1]
        self.outperformance = self.performance - self.results["log_cumm_return"].iloc[-1]

        if display == True: 
            print("RESULTS {} | {} |".format(self.name, self.symbol))
            print("Performance: {}".format(np.round(self.performance,4)))
            print("Outperformance: {}".format(np.round(self.outperformance,4)))
    
    def plot(self, chart_type = "cumm"):
        if chart_type == "cumm":
            self.results.loc[:,["log_cumm_return", "log_strategy_cumm_return"]].plot(figsize = (12,8), title = "{} | SMA{} - SMA{}".format(self.symbol, self.ma_var_1, self.ma_var_2))
        if chart_type == "trade":
            self.results.loc[:,["Close", "SMA{}".format(self.ma_var_1),"SMA{}".format(self.ma_var_2),"position"]].plot(figsize = (12,8), title = "{} | SMA{} - SMA{}".format(self.symbol, self.ma_var_1, self.ma_var_2), secondary_y = "position")


#%%        
# IDEAS // IMPROVEMENT AREAS --------------------------------------        
# Create a separate class for the results to improve consistency 
# TODOs -----------------------------------------------------------
# TODO - fully implement results class 
# TODO - check return calculations 
# TODO - better formatting 
