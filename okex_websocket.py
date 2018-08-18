import hashlib
import json
import traceback
import websocket
from time import sleep
from threading import Thread

# API Doc https://github.com/okcoin-okex/OKEx.com-api-docs

OKEX_HOST = 'wss://real.okex.com:10441/websocket'               # OKEX  exchange

###################################################################################
class OKEXWebSocket(object):    

    """
    Some of the Universial functions        
    """

    def __init__(self):
        self.host = ''         
        self.apiKey = ''        
        self.secretKey = ''     
        self.ws = None          
        self.thread = None      

    def reconnect(self):
        # To close the previous session
        self.close()
        # To reconnect using the following para
        self.ws = websocket.WebSocketApp(self.host, 
                                         on_message=self.onMessage,
                                         on_error=self.onError,
                                         on_close=self.onClose,
                                         on_open=self.onOpen)        
        self.thread = Thread(target=self.ws.run_forever)
        self.thread.start()
    
    def connect(self, apiKey, secretKey, trace=False):
        """
        :param apiKey   : API key
        :param secretKey: key
        :param trace    : If websocket journal activities need to be tracked. Check StreamHandler for it.
        :return:
        """
        # Renew websocket API info
        self.host = OKEX_HOST
        self.apiKey = apiKey
        self.secretKey = secretKey
        # Websocket journal
        websocket.enableTrace(trace)
        self.ws = websocket.WebSocketApp(self.host, 
                                             on_message=self.onMessage,
                                             on_error=self.onError,
                                             on_close=self.onClose,
                                             on_open=self.onOpen)        
            
        self.thread = Thread(target=self.ws.run_forever)
        self.thread.start()

    def readData(self, evt):
        """
        To decode received Websocket raw data
        :param evt:
        :return:
        """
        data = json.loads(evt)
        return data

    def close(self):
        if self.thread and self.thread.isAlive():
            print(u'OKEX.close')
            self.ws.close()
            self.thread.join()
    def onMessage(self, ws, evt):
        """
        Websocket Message
        """
        print(u'OKEX.onMessage:{}'.format(evt))
        
    def onError(self, ws, evt):
        print(u'OKEX.onError_API:{}'.format(evt))

    def onClose(self, ws):
        print(u'OKEX.Websocket.onClose')
        
    def onOpen(self, ws):
        print(u'OKEX.Websocket.onOpen')
        
    def generateSign(self, parameters):
        signin = []
        for key in sorted(parameters.keys()):
            signin.append('%s=%s' %(key, parameters[key]))
        signin.append('secret_key=%s' %self.secretKey)
        sign = '&'.join(signin)
        return hashlib.md5(sign.encode('utf-8')).hexdigest().upper()

    def sendRequest(self, channel, parameters):
        print(u'OKEX.sendRequest:{}'.format(channel))
        parameters['api_key'] = self.apiKey
        parameters['sign'] = self.generateSign(parameters)
        request = {}
        request['event'] = 'addChannel'
        request['channel'] = channel        
        request['parameters'] = parameters
        
        request_package = json.dumps(request)
        
        try:
            self.ws.send(request_package)
        except websocket.WebSocketConnectionClosedException as ex:
            print(u'OKEX.TradingRequest Exception:{}'.format(str(ex)),file=sys.stderr)


    def sendDataRequest(self, channel):

        print(u'OKEX.sendDataRequest:{}'.format(channel))
        request = {}
        request['event'] = 'addChannel'
        request['channel'] = channel
        request_package = json.dumps(request)
        

        try:
            self.ws.send(request_package)
        except websocket.WebSocketConnectionClosedException as ex:
            print(u'OKEX.sendDataRequest Exception:{},{}'.format(str(ex),traceback.format_exc()), file=sys.stderr)
        except Exception as ex:
            print(u'OKEX.sendDataRequest Exception:{},{}'.format(str(ex),traceback.format_exc()), file=sys.stderr)

    def sendHeartBeat(self):
        """
        HeartBeat to maintain connection with the API
        """
        HeartBeatPing = {'event': 'ping'}

        try:
            print(u'OKEX.sendHeartBeat')
            HeartBeatPing_package = json.dumps(HeartBeatPing)
            self.ws.send(HeartBeatPing_package)
        except websocket.WebSocketConnectionClosedException as ex:
            print(u'OKEX.sendHeartBeat Exception:{}'.format(str(ex)), file=sys.stderr)

    def login(self):

        print(u'OKEX.login()')
        parameters = {}
        parameters['api_key'] = self.apiKey
        parameters['sign'] = self.generateSign(parameters)
        
        request = {}
        request['event'] = 'login'
        request['parameters'] = parameters
        

        request_package = json.dumps(request)

        try:
            self.ws.send(request_package)
            return True
        except websocket.WebSocketConnectionClosedException as ex:
            print(u'OKEX.login encounter exceptions:{},{}'.format(str(ex), traceback.format_exc()), file=sys.stderr)
            return False


########################################################################
class OKEXSpotApi(OKEXWebSocket):
    """OKEX Spot trade"""

    def __init__(self):
        """Constructor"""
        super(WsSpotApi, self).__init__()

    def ChannelSpotTicker(self, symbol):
        print(u'OKEX.ChannelSpotTicker:{}'.format(symbol))
        channel = 'ok_sub_spot_%s_ticker' %symbol
        self.sendDataRequest(channel)

    def ChannelSpotDepth(self, symbol, depth=0):
        """Spot Depth of the Market"""
        print(u'OKEX.ChannelSpotDepth:{}'.format(symbol))

        channel = 'ok_sub_spot_%s_depth' %symbol
        if depth:
            channel = channel + '_' + str(depth)
        self.sendDataRequest(channel)

    def ChannelSpotDeals(self, symbol):

        print(u'OKEX.ChannelSpotDeals:{}'.format(symbol))
        channel = 'ok_sub_spot_%s_deals' %symbol
        self.sendDataRequest(channel)

    def ChannelSpotChart(self, symbol, period):

        print(u'OKEX.ChannelSpotChart:{} {}'.format(symbol,period))
        channel = 'ok_sub_spot_%s_kline_%s' %(symbol, period)
        self.sendDataRequest(channel)

    def spotUserInfo(self):

        channel = 'ok_spot_userinfo'
        self.sendRequest(channel, {})


class OKEXFuturesApi(OKEXWebSocket):

    def __init__(self):
        """Constructor"""
        self.apiKey = ''  
        self.secretKey = ''  
        self.ws = None  
        self.active = False  
        self.use_lever_rate = 10
        self.trace = False

    def subsribeFutureTicker(self, symbol, contract_type):
        req = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_ticker_%s'}" % (symbol, contract_type)
        self.ws.send(req)

    def ChannelFutureChart(self, symbol, contract_type, time_period):
        req = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_kline_%s_%s'}" % (
        symbol, contract_type, time_period)
        self.ws.send(req)

    def ChannelFutureDepth(self, symbol, contract_type):
        req = "{'event':'addChannel','channel':'ok_sub_future_%s_depth_%s_usd'}" % (symbol, contract_type)
        self.ws.send(req)

    def ChannelFutureDepth20(self, symbol, contract_type):
        req = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_depth_%s_20'}" % (symbol, contract_type)
        self.ws.send(req)

    def ChannelFutureTrades(self, symbol, contract_type):
        req = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_trade_%s'}" % (symbol, contract_type)
        self.ws.send(req)

    def ChannelFutureIndex(self, symbol):
        req = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_index'}" % (symbol)
        self.ws.send(req)

    def futureChannelIndex(self, symbol):
        channel = 'ok_sub_futureusd_%s_index' % symbol
        self.sendTradingRequest(channel, {})

    def futureUserInfo(self):
        channel = 'ok_futureusd_userinfo'
        self.sendTradingRequest(channel, {})
