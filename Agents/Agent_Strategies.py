'''' This file contains all agent straegies'''
from random import randrange
import random
import operator

import sys
import os
sys.path.append('/'.join(os.getcwd().split('/'))+'/LOB')
sys.path.append('/'.join(os.getcwd().split('/')[:-1])) #Allows us to import from any folder in the main directory
from orderbook_timed import OrderBook   #This one also accounts for the current time



#@param side: 0=buy, 1=sell

''' Defining Agent Trading Methods --- For LIMIT orders '''


''' Random Trader - Take input variables, then randomly create order that is x-away from current price.
    The random trader aims to trade a qty that is inversely proportional to its trading frequency.
    Similarly, this is also true for the price difference between the current price and the agents trade price.

    @param agent_id: id of agent trading
    @param agent_info: List containing details and parameters of all agents within the simulation.
    @param last_price: Last traded price
    @praram rng: Random seed - So we can reproduce results

    @Retrun qty: Quantity of asset traded
    @Return direction: Direction of trade. i.e Buy or Sell, Where 0=buy, 1=sell
    @Return price: Price of trade placed
'''
def random_trader_limit_order(agent_id, agent_info, last_price, rng):
    normal=agent_info[agent_id][1]; #Paramter contained within agent info - Distribution centre
    sd= agent_info[agent_id][2] #Paramter contained within agent info - Trading Frequency
    qty=0
    while qty==0:
        qty= int(rng.chisquare(sd)/100)
    price= int(rng.normal(loc=normal, scale=sd, size=None))

    direction= 1 if price<0 else 0
    price=int(price/1000)
    price+=last_price
    return qty, direction, price


''' Trend Following Agent - Take input variables, then determine if the nth previous trade is larger or smaller than the current price.
    Trade accordingly. i.e Sell if the current price is smaller than the previous. 

    @param agent_id: id of agent trading
    @param agent_info: List containing details and parameters of all agents within the simulation.
    @param last_price: Last traded price
    @praram rng: Random seed - So we can reproduce results

    @Retrun qty: Quantity of asset traded
    @Return direction: Direction of trade. i.e Buy or Sell, Where 0=buy, 1=sell
    @Return price: Price of trade placed
'''
def trend_follower_limit_order(agent_id, agent_info, transactions, last_price, rng ):
    num_trades=agent_info[agent_id][1]  #Paramter contained within agent info - Trading Frequency, this sets how many previous trades we look back on
    try:
        slope=last_price - transactions[-num_trades-1][4]
    except:
        #print("History length not sufficient for this agent to make a decision")
        slope=0
    if slope==0:
        return 0, 'NOTHING', last_price 
    else:
        direction= 1 if slope<0 else 0
        sd= agent_info[agent_id][2]
        qty= int(rng.chisquare(sd)/100)
        price=  qty*-1 if direction=='SELL' else qty
        price=int(price/1000)
        price+=last_price

        return qty, direction, price


''' Mean Reverting Agent - Take input variables, then calculate the mean of the n previous trades.
    Trade accordingly. i.e Sell if the current price is larger than the mean of the last n trades.
    
    @param agent_id: id of agent trading
    @param agent_info: List containing details and parameters of all agents within the simulation.
    @param last_price: Last traded price
    @praram rng: Random seed - So we can reproduce results

    @Retrun qty: Quantity of asset traded
    @Return direction: Direction of trade. i.e Buy or Sell, Where 0=buy, 1=sell
    @Return price: Price of trade placed
'''
def mean_reverting_limit_order(agent_id, agent_info, transactions, last_price, rng):
    sd= agent_info[agent_id][2] #Paramter contained within agent info - Trading Frequency, sets the sd to calculate the trade size
    num_trades=agent_info[agent_id][1] #Paramter contained within agent info - Trading Frequency, this sets how many previous trades we look back on
    prices=[row[4] for row in transactions[-num_trades:]]  #This gets all the previous prices
    mean= int(sum(prices) / len(prices))

    qty= int(rng.chisquare(sd)/100)

    direction= 1 if mean<last_price else 0
    price=mean
    return qty, direction, price



''' Spike Agent - Submitts a large order to "eat" the orderbook on a certain side.
There are more details I will fill in later
    
    @param agent_id: id of agent trading
    @param agent_info: List containing details and parameters of all agents within the simulation.
    @param last_price: Last traded price
    @praram ob: Orderbook

    @Retrun qty: Quantity of asset traded
    @Return direction: Direction of trade. i.e Buy or Sell, Where 0=buy, 1=sell
    @Return price: Price of trade placed
'''
def spike_limit_order(agent_id, agent_info, transactions, last_price, ob):
    print("INSIDE SPIKE")
    spike_size=agent_info[agent_id][1][0]
    spike_ratio=agent_info[agent_id][1][1]

    #Get buy and sell from orderbook
    buys, sells = OrderBook.render_orders(ob)
    # Cases where there are not enough buys or sells tfor the function to work correctly. i.e Can't figure out how to move the price
    if len(buys)<2 and len(sells)<2:
        print("No Orders Anywhere - we can push in a random direction")
        price=last_price + int(rng.normal(loc=last_price, scale=last_price*spike_ratio, size=None))
        qty=[row[2] for row in transactions[-spike_size*500:]]  #This gets all the previous quantities
        direction=rng.choice([0,1])
        push_direction='UPWARD' if direction==0 else "DOWNWARD"
        print("Spike move it: ", push_direction)
        return qty, direction, price

    if len(buys)<2:
        print("There are no BUY orders - Time to SPIKE - DOWNWARD")
        direction= 1 #Sell to all of the waiting buys
        price= int(sells[-1][0][0]*spike_ratio)
        volume_sum_sells= sum(row[0][1] for row in sells)
        qty= int(volume_sum_sells * 1/spike_size)
        return qty, direction, price

    if len(sells)<2:
        print("There are no SELL orders - Time to SPIKE - UPWARD")
        direction= 0 #Buy up all of the waiting sells
        price= int(buys[0][0][0]*spike_ratio)
        volume_sum_buys= sum(row[0][1] for row in buys)
        qty= int(volume_sum_buys * spike_size)
        return qty, direction, price

    # There are enough orders for us to calculate which direction to push price, and by how much
    else:
        #Get spread
        spread= int(sells[-1][0][0] - buys[0][0][0])

        #Calculate size of volume for each side
        volume_sum_sells= sum(row[0][1] for row in sells)
        volume_sum_buys= sum(row[0][1] for row in buys)
        #Calculate how far you can move it  in each direction
        move_sell= sells[0][0][0] - sells[-1][0][0]
        move_buy= buys[0][0][0] - buys[-1][0][0]

        #Calculate volume/movement ratio - smaller is better
        sell_move_ratio = volume_sum_sells/move_sell if move_sell!=0 else 0
        buy_move_ratio = volume_sum_buys/move_buy if move_buy!=0 else 0
        

        #If sell ratio is smaller - that means we will buy up all of the sell orderbook
        #This will push the price UPWARD
        if sell_move_ratio < buy_move_ratio :
            direction= 0 #Buy up all of the waiting sells
            price= int(sells[0][0][0]*spike_ratio)
            qty= int(volume_sum_sells * spike_size)
            print("Push price upwards")
            return qty, direction, price

        else:
            direction= 1 #Sell to all of the waiting buys
            price= int(buys[-1][0][0]*1/spike_ratio)
            qty= int(volume_sum_buys * spike_size)
            print("Push price downwards")
            return qty, direction, price
        return qty, direction, price
    



#########################################################################
#########################################################################

#       Market Order Functions - The work similar to above

#########################################################################
#########################################################################

#These functions are essentially the same as above, however they only output 'trade_size', 'direction'
#This is because we assume a thin orderbook, in which a single quantity unit moves the price up/down an increment. 

''' Defining Agent Trading Methods --  Market Orders '''
def random_trader(agent_id, agent_info, rng):
    normal=agent_info[agent_id][1]; sd= agent_info[agent_id][2]
    trade_size=0
    while trade_size==0:
        trade_size= int(rng.normal(loc=normal, scale=sd, size=None))

    direction= "SELL" if trade_size<0 else 'BUY'
    return trade_size, direction


def trend_follower(agent_id, agent_info, transactions, rng ):
    num_trades=agent_info[agent_id][1]
    try:
        slope=transactions[-1][-1] - transactions[-num_trades-1][-1]
    except:
        print("History length not sufficeint for this agent to make a decision")
        slope=0
    if slope==0:   #Do nothing - but wwe will keep a log of this "transaction" just for de-bugging or history
        return 0, 'NOTHING'
    else:
        direction= "SELL" if slope<0 else 'BUY'
        normal=agent_info[agent_id][1]; sd= agent_info[agent_id][2]
        trade_size= int(rng.chisquare(sd))
        trade_size=  trade_size*-1 if direction=='SELL' else trade_size
        return trade_size, direction


def mean_reverting(agent_id, agent_info, transactions, rng):
    normal=agent_info[agent_id][1]; sd= agent_info[agent_id][2]; num_trades=agent_info[agent_id][1]
    prices=[row[3] for row in transactions[-num_trades:]]
    mean= sum(prices) / len(prices)

    if prices[-1]==mean:
        return 0, 'NOTHING'
    else:

        trade_size= int(rng.chisquare(sd))
    
        direction= "BUY" if prices[-1]<mean else 'SELL'
        trade_size=  trade_size*-1 if direction=='SELL' else trade_size
    
        #Check that we're not going to "overshoot" the mean
        distance_to_mean=prices[-1]-mean
        trade_size= trade_size if trade_size>distance_to_mean   else distance_to_mean*-1
    return trade_size, direction


