''' This code is used to create a simulated market
It consists of n random agents, that place market orders of size X and frequency f(1/X)
price movements are are immediate as we assume there is a very thin orderbook.

i.e BUY(2) raises the price by 2 units, while SELL(2) reduces the price by 2 units
'''


'''We will have a list of agents that MAY make a trade at a particular time
Each agent will have a probability of making a trade, probability of buy/sell 
and an amount range.
This amount range will be inversely proportional to the frequency of their trades'''
import numpy as np
from Agents.Agent_Generation import *
from Agents.Agent_Timings import *
from Main_Simulator.Simulator import *
from Analysis.Results_and_Analysis import *
from utils.utils import *
import os


##################################
####### SETTING PARAMETERS #######
##################################
simulation_time=1000*60*10 #Each time-step represents 1 millisecond. i.e 1000*60 is One Minute
use_historical_prices=False #Allows user to input an array of historical prices. If False no history will be used.
current_price=1000  #This is the initial price - if you do not submit a historical price variable
historical_prices=np.array([0,100]) #This is a historical_prices variable - must be an array
random_seed=100 #This our random seed - so that we may "fix" our simulation, allowing us to run comparable experiments
rng = np.random.default_rng(random_seed) #This is a better way of fixing the seed, as we may introduce other variable, with different seed fixes

# Saving Data #
save_transaction_df=True
save_path=os.getcwd()+'/Output' #.../Market_Simulator_dev/Output'
print("ASAVE PATH",save_path)
file_name='test'
file_type='bz2'

################################
####### AGENT GENERATION #######
################################
agent_info=[] #Initialise an empTy list of agents

#Generate agent information; agent_id,agent_info - information about all created agents, 
#    parameters [ min_frequency - minimum wake frequency, this is also the time-period which calculations are done for trEnd/mean agents
#    max_freq  - this is the maximum amount of time the agent will wait before waking up]
#    linear - as agents are generated in a for loop process, we can specify if the "wake_frequency" is spaced linearly, or on the logspace

'''Generate Random Agents '''
agent_info=generate_agent_info(num_agents=100,agent_info=agent_info, min_freq=1, max_freq=150, linear=True)
''''Generate Trend Following Agents'''
agent_info= generate_agent_info_trend(num_agents=20, agent_info=agent_info, min_freq=2, max_freq=2500, linear=True)
'''Generate Mean Reverting Agents'''
agent_info= generate_agent_info_mean(num_agents=20, agent_info=agent_info, min_freq=2, max_freq=2500, linear=True)







#### GET ALL WAKE TIMES FOR AGENTS ####
all_wake_times= generating_agent_wake_times(agent_info, simulation_time, rng)

#### CREATE WAKE TIMINGS FOR THE SIMULATOR TO USE ####
wake_up_instances= combine_agent_wake_times(all_wake_times)




################################
####### MAIN SIMULATION ########
################################

### SET INITIAL MARKET CONDITIONS ####
if use_historical_prices:
    transactions=historical_price(historical_prices)
    current_price=transactions[-1][-1]
    print(transactions)
else:
    transactions=[]
    current_price=current_price
##


##### $$$$$ RUN THE MAIN SIMULATION  $$$$$ #####
current_price, transactions = run_market_sim(current_price,  transactions, simulation_time, wake_up_instances, agent_info, rng)
#print(current_price)
#print(transactions)
print(f'\nNumber of Trades: {len(transactions):,}' )




######################################
####### Plot/ Analyse Results ########
######################################
transactions_df, final_df= summarise_results(transactions, agent_info)


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