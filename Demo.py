from okex_websocket import *


apiKey = ''
secretKey = ''

# To initialize what API to open
API = OKEXFuturesApi()
#API = OKEXSpotApi()

API.connect(apiKey, secretKey, True)

sleep(3)

API.login()

# OKEX data format for parameters

#SYMBOL = ["btc","ltc","eth","etc","bch","eos","xrp","btg"]
#TYPES = ["this_week", "next_week", "quarter"]
#CHART_CANDLE_TYPES = ["1min","3min","5min","15min","30min","1hour","2hour","4hour","6hour","12hour","day","3day","week"]


# SPOT Channel examples:




#API.ChannelSpotTicker("bch_btc")
#API.ChannelSpotDepth("bch_btc")
#API.ChannelSpotDepth("bch_btc", 5)
#API.ChannelSpotDeals("bch_btc")
#API.ChannelSpotChart("bch_btc","30min")


# Future Channel examples:



API.ChannelFutureDepth("btc","this_week")
#API.ChannelFutureDepth("btc","this_week", 5)
#API.ChannelFutureTrades("btc","this_week")
#API.ChannelFutureIndex("btc")
#API.ChannelFutureForecast_price("btc")

while 1:
    API.sendHeartBeat()
    sleep (100)