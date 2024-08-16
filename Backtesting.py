## BACKTESTING IMPLEMENTATION
#%%
import Classes as c
import numpy as np 
import pandas as pd 
import yfinance as yf

#%%
test = c.SMA("MSFT",10,50,"2022-01-01")


#%%
stocklist = ["AAPL", "IBM", "MSFT"]

combinations = np.arange(5,100,5)

#%%
symbol = []
sample_list = []
performance = []
outperformance = []
i_combinations = []
j_combinations = []


for stock in stocklist: 
    for comb_i in combinations: 
        for comb_j in combinations: 
            if comb_i <= comb_j:
                # append name 
                symbol.append(stock)

                # run test 
                sample = c.SMA(stock,comb_i,comb_j,"1990-01-01")
                sample.run(display = False)
                sample_list.append(sample)
                
                # append results 
                performance.append(sample.performance)
                outperformance.append(sample.outperformance)

                # append combination
                i_combinations.append(comb_i)
                j_combinations.append(comb_j)

#%%

dict = {
    'symbol':symbol,
    'sample':sample_list,
    'performance':performance, 
    'outperformance':outperformance, 
    'i':i_combinations, 
    'j':j_combinations
}

results = pd.DataFrame(dict)

#%%