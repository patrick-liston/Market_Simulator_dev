'''' This file contains all agent straegies'''
from random import randrange
import random
import operator



''' Defining Agent Trading Methods '''
def random_trader(agent_id, agent_info, rng):
    normal=agent_info[agent_id][1]; sd= agent_info[agent_id][2]
    trade_size=0
    while trade_size==0:
        trade_size= int(rng.normal(loc=normal, scale=sd, size=None))

    direction= "SELL" if trade_size<0 else 'BUY'
    return trade_size, direction


def trend_follower(agent_id, agent_info, transactions ):
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


def mean_reverting(agent_id, agent_info, transactions):
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

