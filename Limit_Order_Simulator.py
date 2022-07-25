#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 22:00:51 2022

@author: patrick
"""

''' This code is used to create a simulated market
It consists of n random agents, that place market orders of size X and frequency f(1/X)
price movements are are immediate as we assume there is a very thin orderbook.

i.e BUY(2) raaises the price by 2 units, while SELL(2) reduces the price by 2 units
'''


import numpy as np
from Agents.Agent_Generation import *
from Agents.Agent_Timings import *
from Main_Simulator.Simulator_LOB import *
from Analysis.Results_and_Analysis import *
from utils.utils import *
import os
from collections import deque

import sys
sys.path.append('/home/patrick/Desktop/PhD/Market_Simulator_dev/LOB')
from orderbook_timed import OrderBook   #This one also accounts for the current time


##################################
####### SETTING PARAMETERS #######
##################################
simulation_time=1000*60*5 #Each time-step represents 1 millisecond. i.e 1000*60 is One Minute
use_historical_prices=False #Allows user to input an array of historical prices. If False no history will be used.
current_price=1000  #This is the initial price - if you do not submit a historical price variable
historical_prices=np.array([0,100]) #This is a historical_prices variable - must be an array
random_seed=100 #This our random seed - so that we may "fix" our simulation, allowing us to run comparable experiments
rng = np.random.default_rng(random_seed) #This is a better way of fixing the seed, as we may introduce other variable, with different seed fixes
save_data=False #If we want to save all the transactions in a csv
record_orderbook=False  #This is for if we want to record each step of the orderbook - saves it in a txt file

# Saving Data #
save_transaction_df=True
save_path=os.getcwd()+'/Output' #.../Market_Simulator_dev/Output'
print("SAVE PATH",save_path)
file_name='test_LOB'
file_type='bz2'




################################
####### AGENT GENERATION #######
################################
##Initial conditions###
num_agents=1000; min_freq=100; max_freq=150000; linear=True
agent_info=[]
#Generate agent information; agent_id, parameter - min_frequency, and trading frequency
'''Generate Random Agents '''
agent_info=generate_agent_info(num_agents,agent_info, min_freq, max_freq, linear)
''''Generate Trend Following Agents'''
agent_info= generate_agent_info_trend(100, agent_info, min_freq=200, max_freq=24000, linear=True)
'''Generate Mean Reverting Agents'''
agent_info= generate_agent_info_mean(100, agent_info, min_freq=200, max_freq=24000, linear=True)

 

#### GET ALL WAKE TIMES FOR AGENTS ####
all_wake_times= generating_agent_wake_times(agent_info, simulation_time, rng)

#### CREATE WAKE TIMINGS FOR THE SIMULATOR TO USE ####
wake_up_instances= combine_agent_wake_times(all_wake_times)



spike_agent=False
'''Generate Spike Agents'''
if spike_agent:
    agent_info= generate_agent_info_spike(1,agent_info, spike_times=[25000,50000,100000,200000], spike_size=[2, 2])
    #Parameters for setting spike sizes, [0] Spike size - qty of the spike, [1] spike_ratio - how much higher or lower than current price
    for i in range(len(agent_info[-1][2])):
        wake_up_instances[agent_info[-1][2][i]]= [agent_info[-1][0]]





################################
####### MAIN SIMULATION ########
################################

### SET INITIAL CONDITIONS ####
if use_historical_prices:
    transactions=deque(historical_price(historical_prices))
    last_price=transactions[-1][-1]
    #transactions_df=pd.DataFrame(transactions,columns=['time','agent','nothing', 'price'])
    # transactions_df['price'].plot()

else:
    max_price=1000
    transactions = []#OrderBook("BTCUSD", max_price=max_price)
    last_price=1000

#        _, buys, sells= OrderBook.render_orders(ob)
#        print("Buys", buys)
#        print("Sells", sells)


##
print("About to start the main simulation...")
#%timeit run_market_sim(last_price,  transactions, sim_time)
last_price, transactions, ob, orders_unedited = run_market_sim_LOB(last_price,  transactions, simulation_time, wake_up_instances, agent_info, rng, record_orderbook)
#print (ob.render())
print(f'\nNumber of Trades: {len(transactions):,}' )
#price=[x+abs(min(price)) for x in price]




######################################
####### Plot/ Analyse Results ########
######################################
transactions_df, final_df= summarise_results_LOB(transactions, agent_info)

plot_simple_human_time(transactions_df, show_plot=True)


if save_data:
    save_data(transactions_df, save_path, file_name, file_type)
    save_transaction_df=True


candle_data= create_candle_df(transactions_df, candle_size='5s') #1Min, 5s, 
print(candle_data)


plot_candles(candle_data, show_plot=True)

plot_simple(transactions_df, show_plot=True)



#IF YOU WANT TO UNZIP THE SAVED FILE USE THE FOLLOWING
    #This will create a file that you can read in with pickle 
#unbz2(path,file)