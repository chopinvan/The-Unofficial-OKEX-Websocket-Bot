
class globalVars():
    pass

Golbal_control = globalVars() #empty object to pass around global state


Golbal_control.apiKey_websocket = 'xxxxxxyourapiKeyfromOKEX'
Golbal_control.secretKey_websocket = 'xxxxxxyoursecretfromOKEX'


Golbal_control.apiKey_restapi = 'xxxxxxyourapiKeyfromOKEX,could be the same as websocket or could be different'
Golbal_control.secretKey_restapi = 'xxxxxxyoursecretfromOKEX,could be the same as websocket or could be different'




Golbal_control.trades_switch = 0           ## To switch on / off trades monitoring

Golbal_control.trades_total = 0           ## To switch on / off trades monitoring
Golbal_control.trades_price = 0  
#Golbal_passing.trades_total_sell = 0           ## To switch on / off trades monitoring

Golbal_control.sanity_check_input_price = 5000

Golbal_control.kill = False

Golbal_control.position_data = {"data": []}


Golbal_control.Current_long_position = -1
Golbal_control.Current_short_position = -1

Golbal_control.Current_resting_position_long = -1
Golbal_control.Current_resting_position_short = -1

Golbal_control.Current_long_position_entry_price = -1
Golbal_control.Current_short_position_entry_price = -1

Golbal_control.Current_long_position_profit = -1
Golbal_control.Current_short_position_profit = -1

Golbal_control.last_orderID = 0  
Golbal_control.onError = 0

Golbal_control.product_name = "btc_usd"
Golbal_control.product_name_channel = "btc"
Golbal_control.product_delivery = "quarter"


Golbal_control.cancel = 0
Golbal_control.kill = False
Golbal_control.position_reset = 0


Golbal_control.buy_amount = 1     #$$$$$$$$$$$$$$$$4       Buy amount is here 
Golbal_control.sell_amount = 1    #$$$$$$$$$$$$$$$$4      Sell amount is here 


Golbal_control.REST_freq = 0.5     #Rest refreshing frequency in seconds 
Golbal_control.Websocket_freq = 0.5    #Websocket register refreshing frequency in seconds. Slower refreshing rate will result orders that submited but not registered internally. So this number should always be smaller than order submition speed


Golbal_control.sendHeartBeat = 30