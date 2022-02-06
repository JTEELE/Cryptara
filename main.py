
#Import libraries and dependencies
print(f'Lets get warmed up..')
from dotenv import load_dotenv
from itertools import product
from panel.interact import interact
import datetime
import os
import random
import pandas as pd
import numpy as np
import warnings
import fear_and_greed
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
from _functions import *

fng = fear_and_greed.get()
fng = fng.description
print(fng)

#The name of this project is 'Cryptara' and the objective of this script is to build a Robo-advisor
name = input("Welcome Crypto Investor, what is your name?")

#Introduction. Have user input their desired upload option. Options include importing a csv or inputting individual tickers.
if name == None:
    print('I respect your privacy, I can call you Nomad for now..')
    name = "Nomad"
if name != "" or name == None:
    # Store user's cash investment.
    print(f"Hello {name}, my name is Cryptara. I make your savings go to good use in the Crypto market..")
    print("You will need an active TradingView account for this script, credentials belong in the env file.")
    data_source=input("There is a prefilled csv list if you choose import, would you like to import a csv file or input your tickers manually? Type: 'import' OR 'input'")
    print(f"{data_source} option has been selected..")
    print(f"")
    investment=input("how much cash would you like to invest?")
    investment = float(investment)
    print('')
    print(f'Once I have your list, this process starts automatically..')
    print(f'I use data from the TradingView API and filter your list, then I apply a built-in technical analysis function to determine which cryptos are good picks at this point in time')
    print(f"Then, I run hundreds of simulations to determine optimal weights for each crypto selection")
    print(f"From there, I will scan multiple exchanges to determine where you could get the most volume for the dollar at that particular time '(based on cross-exchange rates)'")
    print(f"Lastly, I will present to you an interactive Dashboard along with my future projections..")

    #User input validation
if data_source == 'import':
    from pathlib import Path
    ticker_data = Path("csv_data/crypto_tickers1.csv")
    print(f'Thanks for using our csv file import option! Let me look through your list and see if I can validate the data..')
if data_source == 'input':
    ticker_1=input("Tell me the first ticker")
    ticker_2=input("Tell me the second ticker")
    ticker_3=input("Tell me the third ticker")
    ticker_4=input("Tell me the fourth ticker")
    ticker_5=input("Tell me the fifth ticker")
    ticker_6=input("Tell me the sixth ticker")
    ticker_7=input("Tell me the seventh ticker")
    ticker_8=input("Tell me the eigth ticker")
    ticker_9=input("Tell me the ninth ticker")
    print("Please upgrade to our Premium version of Cryptana to input more than nine tickers.")
    ticker_data = ([ticker_1,ticker_2,ticker_3,ticker_4,ticker_5,ticker_6,ticker_7,ticker_8,ticker_7,ticker_8,ticker_9])
    print(f'Got it. Give me a minute to make sure these tickers are valid')
if data_source != 'import':
    if data_source != 'input':
        data_source = input('Please try again..')

warnings.filterwarnings('ignore')
# %matplotlib inline
exchange = 'BINANCE'

#Create TradingView variable and activate env variables
print(f'Trading View is my trusted partner, together we will see where your money should go')
from tvDatafeed import TvDatafeed,Interval
load_dotenv()
tradev_id = os.getenv("username")
tradev_secret_key = os.getenv("password")

#Log into TradingView
tv = TvDatafeed(tradev_id, tradev_secret_key, chromedriver_path=None)
print('TradingView Authentication is successfull')
print('')

ticker_data = Path("csv_data/crypto_tickers1.csv")
ticker= pd.read_csv(ticker_data, header=None)
ticker_df = pd.DataFrame(ticker)
my_crypto_list = ticker_df[0].tolist()
screener="CRYPTO"
exchange="BINANCE"
df_daily = pd.DataFrame()
print(f"Nice work! No issues have been identified with your list, let me look into these and get back to you. This could take up to 20 min..")

#Get historical pricing information for total population
print(f'Extracting price history..')
try:
    for ticker in my_crypto_list:
        data = tv.get_hist(
            symbol=ticker,
            exchange=exchange,
            interval=Interval.in_daily,n_bars=500)
        df_daily = df_daily.append(data)
except:
    pass
print(f'finished extracting historical prices..')


#Grab indicator recommendations from Trading View API
print(f'Risk protocol: Filtering by analyst recommendations')
print('')
from tradingview_ta import TA_Handler, Interval, Exchange
staging_df = pd.DataFrame()
ticker_df_daily = pd.DataFrame()
for ticker in my_crypto_list:
    try:
        data = (TA_Handler(symbol=ticker,screener=screener,
                           exchange=exchange,interval=Interval.INTERVAL_1_DAY ).get_analysis().summary)
        symbol = ticker
        staging_df = list(data.values())
        final_df = (pd.DataFrame((data), index={ticker}))
        ticker_df_daily = ticker_df_daily.append(final_df)
    except:
        pass
print(f'finished extracting analyst recommendations..')


#Filter imported list by analyst recommendations
print(f'We checked what the top analysts are saying about each crypto in your list')
print('')
print(f'To reduce program speed, Cryptara will only analyze cryptos that meet a BUY or NEUTRAL classification')
initial_drop = ticker_df_daily.loc[ticker_df_daily['RECOMMENDATION']=='SELL']
initial_pass_prime = ticker_df_daily.loc[ticker_df_daily['RECOMMENDATION']=='BUY']
initial_pass_subprime = ticker_df_daily.loc[ticker_df_daily['RECOMMENDATION']=='NEUTRAL']

#initial_drop = initial_indicator['RECOMMENDATION'].str.contains('SELL')
buy_count = initial_pass_prime['RECOMMENDATION'].count() + initial_pass_subprime['RECOMMENDATION'].count()
sell_count = initial_drop['RECOMMENDATION'].count()
print('Here are the initial findings:')
print('')
print(f'It is not a good time to invest in {sell_count} of the cryptos from your list')
print(f'These {sell_count} cryptos are not in a buying position')
print(initial_drop['RECOMMENDATION'])
print(f'These {sell_count} cryptos have been dropped from consideration..')
print('')
print('')
print(f'Moving on, our initial inidicator data suggest {buy_count} cryptos from your list should be considered for further analysis:')
print('Here they are:')
print('Our Prime candidates that are in buy positions are:')
print(initial_pass_prime['RECOMMENDATION'])
print('')
print('And these are neutral for now, we can reserve for later if we need additional cryptos for analysis')
print(initial_pass_subprime['RECOMMENDATION'])

#Extract index values for the tickers that are prime and subprime and format data for further analysis. 
print(f'Nice work, {name}, you found {buy_count} cryptos that might be good investments this week!')
initial_pass_prime.reset_index(inplace=True)
initial_pass_prime = initial_pass_prime['index']
initial_pass_subprime.reset_index(inplace=True)
initial_pass_subprime = initial_pass_subprime['index']
staging_df = pd.DataFrame()
staging_df1 = pd.DataFrame()
prime_df = pd.DataFrame()
subprime_df = pd.DataFrame()
print(f'Lets see what Cryptara thinks about these cryptos..')
print(f'')

#Run a for loop through prime and subprime cryptos and pull in all oscilattor data for technical analysis
#Prime cryptos
print(f'Extracting oscillator data from TradingView for built in technical analysis test...')
for ticker in initial_pass_prime:
    try:
        data = (TA_Handler(symbol=ticker,screener=screener,
                           exchange=exchange,interval=Interval.INTERVAL_1_DAY ).get_analysis().indicators)
        symbol = ticker
        staging_df = list(data.values())
        final_df = (pd.DataFrame((data), index={ticker}))
        prime_df = prime_df.append(final_df)
    except:
        pass

#Sub-prime cryptos
for ticker in initial_pass_subprime:
    try:
        data = (TA_Handler(symbol=ticker,screener=screener,
                           exchange=exchange,interval=Interval.INTERVAL_1_DAY ).get_analysis().indicators)
        symbol = ticker
        staging_df1 = list(data.values())
        final_df = (pd.DataFrame((data), index={ticker}))
        subprime_df = subprime_df.append(final_df)
    except:
        pass
print('Extracted oscillator data, initializing technical analysis test on key trend indicators..')
prime_df.head(3)

#Extract oscillator information for all cryptos that meet the 'buy threshold'  
crypataras_picks = []
print(f'Determining which cryptos are in an optimal buying position based on trend indicators...')
print('Relative Strength Index (RSI), Moving Average Covergence and Divergence (MACD), Stachator positioning and the Awesome Oscillators')
print(f'By doing this, we can see which cryptos are currently overbought or oversold based on historical prices..')
print(f'')
def strong_performers():
    for i, j in prime_df.iterrows():
        if j['RSI'] > 45 and j['RSI'] < 90:
            print(f'{i} has passed the rsi_test, moving to moving average covergence and divergence analysis..')
            if j['MACD.macd'] > 0 and j['MACD.macd'] < 40:
                print(f'{i} has passed our moving average covergence and divergence analysis, moving to stochator analysis..')
                if j['Stoch.K'] > 35 and j['Stoch.K'] < 85:
                    if j['Stoch.D'] > 40 and j['Stoch.D'] < 85:
                        if j['Stoch.RSI.K'] > 30 and j['Stoch.RSI.K'] < 80:
                            print(f'{i} has passed our multiple stochator analysis, testing the Awesome Oscillators..')
                            if j['AO'] > 0 and j['AO'] < 55:
                                if i not in crypataras_picks:
                                    print(f'Cryptara has selected {i} ')
                                    crypataras_picks.append(i)
                                
    else:
        print(f'FAIL! dropping crypto from further consideration..')

strong_performers()
initial_count = len(crypataras_picks)
print(f'')
print('Technical Analysis test is complete.')
print('')
print('Cryptara has analyzed key technical indicators and suggest that the following crypto assets')
print('are in optimal buying positions')
print('')
if len(crypataras_picks) >1:
    print(f'Cryptara chooses: {crypataras_picks}')
else:
    print('Its not a good time to invest in Crypto, please try again later..')

crypataras_picks = ['BTCUSD','ETHUSD','DOGEUSD','LTCUSD','ZRXUSD']

try:
    # population_check(crypataras_picks)
    # print(f'')
    # print(f'Here are the final Cryptara picks:')
    # print(f'')
    # # csv_export = pd.DataFrame(crypataras_picks)
    # # csv_export.to_csv('csv_data/cryptaras_final_cryptos.csv')
    # print(f'Extracting most recent prices..')
    final_crypto_df = pd.DataFrame()
    bars= 1000
    for all_picks in crypataras_picks:
        picks_df = tv.get_hist(symbol=all_picks,
                            exchange=exchange,
                            interval=Interval.in_daily,
                            n_bars=bars)
        final_crypto_df = final_crypto_df.append(picks_df)
    print(f'Give me a moment while I reformat some datasets to obtain an optimal performance strategy..')
    portfolio_allocation(final_crypto_df)
except:
    print('Stopping analysis..')
