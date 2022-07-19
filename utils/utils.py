''' This script contains all utility functions for the simulator
It also imports all packages that may be used in the course of using this simulator '''

from random import randrange
import random
import operator
from operator import itemgetter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy.stats import linregress
import sys
import itertools

import os
import sys


''' These functions are used to plot with the current date and time'''
import time
from datetime import datetime
def current_milli_time():
    return round(time.time() * 1000)

#This is used to convert the epoch time to a human readable time - for later analysis
def convert_to_human_time(time, simulation_start_time):
    return datetime.fromtimestamp((time+simulation_start_time)/1000).strftime('%Y-%m-%d %H:%M:%S.%f')



def convert_array_to_list_of_lists(arr):
    list_of_lists = list()
    for row in arr:
        list_of_lists.append(row.tolist())
    return list_of_lists


'''Functions for generating historical prices'''
def historical_price(historical_prices):
    length=len(historical_prices)#.shape[0]
    historical_transactions = np.zeros((length,4))
    historical_time=[i*-1 for  i  in list(reversed(range(length)))]
    historical_transactions[:,-1]=historical_prices
    historical_transactions[:,0]=historical_time
    historical_transactions[:,1]=[-999]*length

    #Convert to list of lists
    return convert_array_to_list_of_lists(historical_transactions)

#This is used to find the main parent directory which the simulator is being run out of
#Allowing us to use this as the "base" path
def get_current_path():
	return ('/'.join(os.getcwd().split('/')[:-1]))