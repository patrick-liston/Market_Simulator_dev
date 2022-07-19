''' This contains the main functions for running the market simulator.

We iterate through all time-steps and call the determine_trader function as;
 we must determine which trader is acting - and hence which agent function to call.
 '''
#NOTE THIS IS A MARKET ORDER SIMULATOR ONLY
from tqdm import tqdm

import os
import sys
sys.path.append('/'.join(os.getcwd().split('/')[:-1])) #Allows us to import from any folder in the main directory
from Agents.Agent_Strategies import * 




def determine_trader(agent_id, agent_info, transactions, rng):
    if agent_info[agent_id][-1]=='Random':
        trade_size, direction = random_trader(agent_id=int(agent_id), agent_info=agent_info, rng=rng)

    elif agent_info[agent_id][-1]=='Trend':
        trade_size, direction = trend_follower(agent_id, agent_info, transactions)

    elif agent_info[agent_id][-1]=='Mean':
        trade_size, direction = mean_reverting(agent_id, agent_info, transactions)

    return trade_size, direction




''' Actual Market Simulator'''
#Iterate through each time_step,
    #If the time-step has orders... let the agent create the order
    #If no agent is making an order at this time, skip this time step .
    #i.e Try: Make orders, Except: pass
def run_market_sim(current_price,  transactions, sim_time, wake_up_instances, agent_info,rng):
    print("Running Market Simulator...")
    for i in tqdm(range(sim_time)):
        try:
            for j in wake_up_instances[i]:

                trade_size, direction= determine_trader(agent_id=j, agent_info=agent_info, transactions=transactions, rng=rng)


                previous_price=current_price
                current_price+=trade_size
                transactions.append([i, int(j),trade_size, current_price])

        except: #This means that we have reached a time-step in which no agent makes a decision - so we skip it
            pass
    return current_price, transactions


