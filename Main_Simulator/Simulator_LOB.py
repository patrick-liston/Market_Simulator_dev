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

sys.path.append('/'.join(os.getcwd().split('/')[:-1])+'/LOB')
sys.path.append('/'.join(os.getcwd().split('/'))+'/LOB')
from orderbook_timed import OrderBook   #This one also accounts for the current time



#@param side: 0=buy, 1=sell
''' This function is used to determine which strategy gets applied/which trading style is used and return the relevant trade information.
    @param agent_id: Agent id
    @param agent_info: List of information about ALL agents within the simulation
    @param transactions: List of all previous trnasactions that have been executed
    @param last_price: Last traded price
    @param orderbook: orderbook object, contains all orders, and is checked for matching trades as soon as a new trade is added
    @praram rng: Random seed - So we can reproduce results

    @Retrun qty: Quantity of asset traded
    @Return direction: Direction of trade. i.e Buy or Sell, Where 0=buy, 1=sell
    @Return price: Price of trade placed

'''
# We return the trade info ONLY
def determine_trader_LOB(agent_id, agent_info, transactions, last_price, orderbook, rng):
    if agent_info[agent_id][-1]=='Random':
        qty, direction, price = random_trader_limit_order(agent_id=int(agent_id), agent_info=agent_info, last_price=last_price, rng=rng)

    elif agent_info[agent_id][-1]=='Trend':
        qty, direction, price = trend_follower_limit_order(agent_id, agent_info, transactions, last_price=last_price, rng=rng)

    elif agent_info[agent_id][-1]=='Mean':
        qty, direction, price = mean_reverting_limit_order(agent_id, agent_info, transactions, last_price=last_price, rng=rng)

    elif agent_info[agent_id][-1]=='Spike':
        print("\nLooking into spike\n")
        #print(agent_id, agent_info, last_price, transactions)
        qty, direction, price = spike_limit_order(agent_id, agent_info, transactions, last_price=last_price, ob=orderbook)
        print("Spike says this:", qty, direction, price)

    return qty, direction, price



''' Actual Market Simulator
#Iterate through each time_step,
    #If the time-step has orders... let the agent create the order
    #If no agent is making an order at this time, skip this time step .
    #i.e Try: Make orders, Except: pass

    
    @param last_price: Last traded price
    @param transactions: List of all previous trnasactions that have been executed
    @param sim_time: Time simulation will run for - maximum time allowed 
    @param wake_up_instances: Dictionary of relevant times, and list of agents to wake. 
    @param agent_info: List of information about all agents within the simulation
    @param rng: Random seed - So we can reproduce results
    @param record_orderbook: Print the current orderbook to a text file. Default=False, set to True if required. (VERY large data files are produced, and simulation time is increased)


    @Retrun last_price: Last traded price
    @Return transactions: List of all previous trnasactions that have been executed
    @Return ob: Orderbook (At final execution only)
    @Return oders_unedited: List containing details or ALL orders that were placed. 
'''


def run_market_sim_LOB(last_price,  transactions, sim_time, wake_up_instances, agent_info, rng, record_orderbook=False):
    #INITIATE ORDEBOOK
    max_price=100000
    orders_unedited=[]
    ob = OrderBook("BTCUSD", max_price=max_price)
    last_price=1000
    orders_unedited=[]

    for i in tqdm(range(sim_time)):
        try:
            for j in wake_up_instances[i]:

                qty, direction, price= determine_trader_LOB(agent_id=int(j), agent_info=agent_info, transactions=transactions, last_price=last_price, orderbook=ob, rng=rng)
                

                if qty:
                    _,last_price, transactions, orders_unedited = ob.limit_order(side=direction, size=qty, price=price, trader=int(j), last_price=last_price,  current_time=i, transactions=transactions, orders_unedited=orders_unedited, print_executions=False)

                #This sections is so that we can record/log the entire orderbook at each change-point. If we want.
                if record_orderbook:
                    with open("/home/patrick/Desktop/PhD/Market_Simulation/Saving_Orderbook/LOB_ouputs.txt", "a+") as text_file:
                        text_file.write("\n\n\nCURRENT_TIME: %s\n %s" %(i,ob.render()))
                    pass

        except:
            #print(i,"No wakes at this time step")
            pass
    return last_price, transactions, ob, orders_unedited















    