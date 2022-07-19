''' These are functions used to both numerically and graphically analyse the results from the simulation
They will take in the raw transactions and created dataframes that are easier for analysis.
Other functions will also help plot some of the results.

This is where we can add more analysis functions'''
import os
import sys 
sys.path.append('/'.join(os.getcwd().split('/')[:-1]))

import pandas as pd
import matplotlib.pyplot as plt
from utils.utils import *
from pathlib import Path

'''Main function for transformaing raw transaction data into a useable dataframe, 
it merges the agent information with trasnactions, as well as computing the "human time" of any trades.
This will be the main dataframe for later analyses'''
def summarise_results(transactions, agent_info):
    #Create df of all transactions
    transaction_df=pd.DataFrame(transactions, columns=['time','agent','amount','price'])
    transaction_df['Human_Time']=[convert_to_human_time(time, current_milli_time()) for time in transaction_df['time']]

    #merge agent infor with transactions to create cleaner df
    agent_info_df=pd.DataFrame(agent_info,columns=['agent_id','normal','wake_freq','type'])
    final_df= pd.merge(transaction_df, agent_info_df, left_on=  ['agent'],right_on= ['agent_id'],how = 'left')
    final_df= final_df[['time','agent','amount','price','type','Human_Time']]
    final_df['previous_price']=final_df['price']-final_df['amount']

    return transaction_df, final_df 



def plot_simple(transaction_df, show_plot=False): 
    plt.plot(transaction_df['price'])
    plt.title('Price - Market Orders only - Size of Trade Porotional to trading Frequency')
    plt.xlabel('Time Step')
    plt.ylabel('Price')
    if show_plot:
        plt.show()



def save_data(data, path, file_name, file_type='.csv'):
    Path(path).mkdir(parents=True, exist_ok=True)
    if file_type=='csv':
        data.to_csv(path+'/'+file_name+ '.'+file_type) 
    else:
        data.to_pickle(path+'/'+file_name+ '.'+file_type)
    print(f"Saved to {file_type}, can be found in folder {path}/{file_name}.{file_type}")
        




import mplfinance as mpf
import plotly.graph_objects as go
import pandas as pd
import bz2
import os


def unbz2(path,file):
    filepath=path+file
    zipfile = bz2.BZ2File(filepath) # open the file
    data = zipfile.read() # get the decompressed data
    newfilepath = filepath[:-4] # assuming the filepath ends with .bz2
    open(newfilepath, 'wb').write(data) # write a uncompressed file

def delete_bz2(path,file):
    filepath=path+file
    os.remove(filepath) # Delete File




def create_candle_df(transactions_df, candle_size='1Min'):
    #CONVERT TO CANDLES
    print("Converting to Candles...")
    transactions_df.index = pd.to_datetime(transactions_df['Human_Time'], unit='ns')
    candle_data=transactions_df[['price']].resample(candle_size).ohlc()
    candle_data.columns = ['open','high','low','close']
    return candle_data


def plot_candles(candle_data, show_plot=False):
    ap = mpf.make_addplot(candle_data)
    mpf.plot(candle_data, type='candle')#, addplot=ap['data']['open'])
    if show_plot:
        mpf.show()

    





# ######################################
# ####### Plot/ Analyse Results ########
# ######################################





# plot_agents=False
# if plot_agents:

#     #transaction_df=pd.DataFrame(transactions, columns=['time','agent','amount','price'])
#     specified_agent=0
#     trade_info=[]
#     for specified_agent in range(len(agent_info)):
#         agent_trades=transaction_df[transaction_df['agent']==specified_agent]
#         agent_trades['amount'].hist()
        
#         ##### Infor for log-log plot of trade_freq vs trade_size
#         trade_frequency_actual=len(agent_trades)/sim_time
#         avg_trade_size=abs(agent_trades['amount']).mean()  #Take abs because sells are negative
#         trade_info.append([specified_agent, trade_frequency_actual, avg_trade_size])
    
    
#     trade_info_df=pd.DataFrame(trade_info, columns=['Agent','trade_freq_actual', 'avg_trade_size'])
#     plt.figure()
#     plt.plot(trade_info_df['trade_freq_actual'],trade_info_df['avg_trade_size'])
#     plt.title('Trade Frequency vs Trade Size')
#     plt.xlabel('Trade Frequency')
#     plt.ylabel('Avg Trade Size')
    
#     plt.figure()
#     plt.plot(np.log(trade_info_df['trade_freq_actual']),np.log(trade_info_df['avg_trade_size']),'bo-')
#     plt.title('Trade Frequency vs Trade Size Logged')
#     plt.xlabel('Trade Frequency (log)')
#     plt.ylabel('Avg Trade Size (log)')
    
#     from scipy.stats import linregress
#     linregress(np.log(trade_info_df['trade_freq_actual']),np.log(trade_info_df['avg_trade_size']))


# ######################################
# ####### Analyse Agents Results #######
# ######################################
# # transaction_df
