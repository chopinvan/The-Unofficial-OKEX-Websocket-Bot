
import json
import datetime
import time
import os
import socket


from okex_rest_FutureAPI import OKCoinFuture
from collections import OrderedDict,defaultdict
from okex_runtime_parameters import * 


apiKey = Golbal_control.apiKey_restapi
secretKey = Golbal_control.secretKey_restapi
position_to_watch = Golbal_control.product_name
okcoinRESTURL = 'www.okex.com'  
Httpsport = 443
Filter = 10

API_REST = OKCoinFuture(okcoinRESTURL,apiKey,secretKey)

class AccountBalanceManager(object):


    def current_holding_info():

        buffer_load = API_REST.future_position(position_to_watch,Golbal_control.product_delivery)
        source = json.loads(buffer_load)
        if (source['result'] == True):
            #print (source['holding'])     # [{'buy_price_avg': 6667.4644948, 'symbol': 'btc_usd', 'lever_rate': 20, 'buy_available': 100, 'contract_id': 201812280000013, 'buy_amount': 100, 'buy_profit_real': -0.00765174, 'contract_type': 'quarter', 'sell_amount': 100, 'sell_price_cost': 6643, 'buy_price_cost': 6667.4644948, 'create_date': 1536915444000, 'sell_price_avg': 6643, 'sell_profit_real': -0.00765174, 'sell_available': 100}]

            Golbal_control.Current_long_position = source['holding'][0]['buy_amount']
            Golbal_control.Current_short_position = source['holding'][0]['sell_amount']

            Golbal_control.Current_resting_position_long = source['holding'][0]['buy_available']
            Golbal_control.Current_resting_position_short = source['holding'][0]['sell_available']

            Golbal_control.Current_long_position_entry_price = source['holding'][0]['buy_price_avg']
            Golbal_control.Current_short_position_entry_price = source['holding'][0]['sell_price_avg']

            Golbal_control.Current_long_position_profit = source['holding'][0]['buy_profit_real']
            Golbal_control.Current_short_position_profit = source['holding'][0]['sell_profit_real']
        else:

            print ("Could not get correct Position data from Rest API")
