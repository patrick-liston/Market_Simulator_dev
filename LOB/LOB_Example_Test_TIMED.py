#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 11:21:07 2022

@author: patrick
"""



# # from collections import deque

# # '''buy=0, sell=1'''
# LOB= OrderBook("BTCUSD", max_price=10, last_price=2)
# ['side', 'size','price', 'agent_id']
# LOB.limit_order( 0, 10, 8, 9999, last_price)
# LOB.limit_order( 1, 5, 9, 9999,last_price)
# #LOB.limit_order( 1, 25, 5, 9999)
# LOB.limit_order( 0, 2, 5, 9999,last_price)
# order_id, last_price = LOB.limit_order( 0, 2, 10, 9999,last_price)

# lveled=LOB.price_points[-1][0]
# dir(lveled)
# lveled.order_id
# lveled.price
# lveled.side
# lveled.size
# lveled.trader


# orders= OrderBook.render(LOB)
# buys, sells= OrderBook.render_orders(LOB)
#  %timeit OrderBook.render_orders(LOB)
# # print(buys)
# # print(sells)

#  buys, sells= OrderBook.render_orders(ob)
#  %timeit OrderBook.render_orders(ob)


# # render_orders

import os
import time
import random
import sys
sys.path.append(os.path.abspath(".."))
sys.path.append('/home/patrick/Desktop/PhD/Market_Simulator_dev/LOB')
#from orderbook import OrderBook
from orderbook_timed import OrderBook   #This one also accounts for the current time

last_price=0
def orderbook_demo():
    import time, random
    ITERS = 1000
    max_price = 10
    ob = OrderBook("FOOBAR", max_price=max_price)
    start = time.time()
    #### Patrick Iniate Variables ####
    transactions=[]
    last_price=0
    for i in range(ITERS):
        os.system("clear")
        buysell, qty, price, trader = random.choice([0,1]), random.randrange(1,50), \
                random.randrange(1,max_price), 'trader %s' % random.randrange(1000)
        print ("NEW ORDER: %s %s %s @ %s" % (trader, "BUY" if buysell==0 else "SELL", qty, price))
        #ob.limit_order(buysell, qty, price, trader,last_price,  current_time=i)
        _,last_price, transactions = ob.limit_order(side=buysell, size=qty, price=price, trader=trader,last_price=last_price,  current_time=i, transactions=transactions)
        print (ob.render())
        #time.sleep(2)

        # _, buys, sells= OrderBook.render_orders(ob)
        # print("Buys", buys)
        # print("Sells", sells)
    return ob, transactions
        #time.sleep(5)


if __name__ == "__main__":
    ob, transactions =orderbook_demo()


import pandas as pd
transactions_df=pd.DataFrame(transactions, columns=['buyer_id', 'seller_id', 'amount', 'currency', 'price', 'buy_sell', 'time_placed', 'executed_time'])



