
#Import libraries and dependencies
from dotenv import load_dotenv
from itertools import product
from panel.interact import interact
import datetime
import os
import random
import pandas as pd
import numpy as np
import warnings
from pathlib import Path
import panel as pn
pn.extension('plotly')
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from plotly.offline import iplot
from plotly.subplots import make_subplots
from panel import widgets
from dotenv import load_dotenv
def population_check(cryptaras_picks):
    if len(cryptaras_picks) > 5:
            cryptaras_picks.remove(random.choice(cryptaras_picks))
            print(f'removed ticker from list to meet maxiumum requirements')

    if len(cryptaras_picks) < 5:
        print('This program requires a minimum of five cryptos to run remaining analysis.')
        computer_selection_1 = subprime_df.sample().reset_index()
        ticker_random_1 = computer_selection_1.iloc[:, 0].tolist()
        string=''.join([str(item) for item in ticker_random_1])
        if string in cryptaras_picks:
            pass
        else:
            cryptaras_picks.append(string)
            print(f'added {string} from BUY list to meet minimum requirements')
            
    if len(cryptaras_picks) < 5:
        print('This program requires a minimum of five cryptos to run remaining analysis.')
        computer_selection_2 = subprime_df.sample().reset_index()
        ticker_random_2 = computer_selection_2.iloc[:, 0].tolist()
        string=''.join([str(item) for item in ticker_random_2])
        if string in cryptaras_picks:
            pass
        else:
            cryptaras_picks.append(string)
            print(f'added {string} from BUY list to meet minimum requirements')
            
    if len(cryptaras_picks) < 5:
        print('This program requires a minimum of five cryptos to run remaining analysis')
        computer_selection_3 = subprime_df.sample().reset_index()
        ticker_random_3 = computer_selection_3.iloc[:, 0].tolist()
        string=''.join([str(item) for item in ticker_random_3])
        if string in cryptaras_picks:
            pass
        else:
            cryptaras_picks.append(string)
            print(f'added {string} from BUY list to meet minimum requirements')
            
    if len(cryptaras_picks) < 5:
        print('This program requires a minimum of five cryptos to run remaining analysis')
        computer_selection_4 = subprime_df.sample().reset_index()
        ticker_random_4 = computer_selection_4.iloc[:, 0].tolist()
        string=''.join([str(item) for item in ticker_random_4])
        if string in cryptaras_picks:
            pass
        else:
            cryptaras_picks.append(string)
            print(f'added {string} from BUY list to meet minimum requirements')

    if len(cryptaras_picks) > 5:
            cryptaras_picks.remove(random.choice(cryptaras_picks))
            print(f'removed ticker from list to meet maxiumum requirements')
    if len(cryptaras_picks) > 5:
            cryptaras_picks.remove(random.choice(cryptaras_picks))
            print(f'removed ticker from list to meet maxiumum requirements')
    if len(cryptaras_picks) > 5:
            cryptaras_picks.remove(random.choice(cryptaras_picks))
            print(f'removed ticker from list to meet maxiumum requirements')
    
    return cryptaras_picks

def portfolio_allocation(final_crypto_df):
    #Step 1: extract exchange and ticker from 'symbol' column into separate columns.
    final_df_cleaner = final_crypto_df
    final_df_cleaner[['exchange', 'ticker']] = final_df_cleaner['symbol'].str.split(':',expand=True)
    #Step 2: Extract ticker and close values, reset index
    final_df_cleaner = final_df_cleaner[['ticker','close']]
    final_df_cleaner = final_df_cleaner[['ticker','close']].reset_index()
    #Step3: Pivot data to make ticker values the column headers
    final_df_cleaner = final_df_cleaner.pivot(index='datetime',
            columns='ticker',
            values='close')
    #Step4: calculate return data
    print('Extracted the historical returns for Cryparas picks..')
    crypto_pick_returns = final_df_cleaner.pct_change().dropna()
    crypto_pick_returns.tail(5)
    #Step5: Calculate Cumulative Returns
    print('Getting a feel for each cryptos LTD cumulative returns ..')
    cumulative_daily_returns = (1 + crypto_pick_returns).cumprod() -1
    cumulative_daily_returns.tail(10)

    #Step5: Calculate Cumulative Returns
    print('Activating Smartfolio program to determine optimal investment strategy..')
    print('')
    print('Logging returns to normalize dataset..')
    log_returns= np.log(abs(cumulative_daily_returns))
    log_returns.tail()

    #Calculate volatility and Initialize variables 
    print(f'Running multiple scenaries to determine appropriate weights for selected cryptos')
    cryptaras_picks = ['BTCUSD','ETHUSD','DOGEUSD','LTCUSD','ZRXUSD']
    num_of_portfolios= 5000
    weight= np.zeros((num_of_portfolios,len(cryptaras_picks)))
    expected_return=  np.zeros(num_of_portfolios)
    expected_volatility= np.zeros(num_of_portfolios)
    sharpe_ratio= np.zeros(num_of_portfolios)
    expected_return
    mean_log_ret= log_returns.mean()
    sigma = log_returns.cov()

    for i in range (num_of_portfolios):
        # generate random weight vectos 
        w= np.array(np.random.random(len(cryptaras_picks)))
            #sum of weights equal to 1 
        w= w/ np.sum(w)
        weight[i,:]= w
        
        # expected log return 
        expected_return[i]= np.sum(mean_log_ret*w)
        
        #expected volatility 
        expected_volatility[i]= np.sqrt(np.dot(w.T,np.dot(sigma,w)))
        
        # sharpe ratio
        sharpe_ratio[i] =  expected_return[i]/expected_volatility[i]
        
    print(f'Here are the weights: ')
    # Weighted portfolio that sharpe ratio
    max_index = sharpe_ratio.argmax()
    weight[max_index,:]

    # Portfolio weights are exported to a csv that can be used for monteclaro simulation
    print(f'Loading Smartfolio weights..')
    print(f'')
    print(f'')
    portfolio_weights = np.array([weight[max_index,:]])
    portfolio_weights = portfolio_weights.tolist() 
    smartfolio_weights = pd.DataFrame(portfolio_weights)
    total_invested=(smartfolio_weights*investment).round(2)
    smartfolio_weights.to_csv('csv_data/smartfolio_weights.csv')
    smartfolio_weights_df = smartfolio_weights
    smartfolio_weights_df.columns = ([cryptaras_picks])
    print(f' ............and DONE!')

    print('')
    print('')
    print(f'At this moment in time, here is how you should allocate your {investment} investment...') 
    print('')
    #print(f' The optimal portfolio weight for '
    print(f'With a {smartfolio_weights.iloc[0][0]:.3f} weight, Cryptara suggests that ${total_invested.iloc[0][0]} should be allocated to {cryptaras_picks[0]}.')
    print('')
    print(f'With a {smartfolio_weights.iloc[0][1]:.3f} weight, Cryptara suggests that ${total_invested.iloc[0][1]} should be allocated to {cryptaras_picks[1]}.')
    print('')
    print(f'With a {smartfolio_weights.iloc[0][2]:.3f} weight, Cryptara suggests that ${total_invested.iloc[0][2]} should be allocated to {cryptaras_picks[2]}.')
    print('')
    print(f'With a {smartfolio_weights.iloc[0][3]:.3f} weight, Cryptara suggests that ${total_invested.iloc[0][3]} should be allocated to {cryptaras_picks[3]}.')
    print('')
    print(f'With a {smartfolio_weights.iloc[0][4]:.3f} weight, Cryptara suggests that ${total_invested.iloc[0][4]} should be allocated to {cryptaras_picks[4]}.')