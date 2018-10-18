import hashlib
import json
import traceback
import websocket
from time import sleep
from threading import Thread
from collections import OrderedDict,defaultdict
from okex_runtime_parameters import * 
import datetime
import zlib
import requests
import sys

# API Doc https://github.com/okcoin-okex/OKEx.com-api-docs

OKEX_FUTURES_HOST = 'wss://real.okex.com:10441/websocket'               # OKEX  exchange
OKEX_SPOT_HOST = 'wss://real.okex.com:10440/websocket'   

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
        Golbal_control.onError = 0
    
    def connect(self, apiKey, secretKey, trace=False):
        """
        :param apiKey   : API key
        :param secretKey: key
        :param trace    : If websocket journal activities need to be tracked. Check StreamHandler for it.
        :return:
        """
        # Renew websocket API info
        self.host = OKEX_FUTURES_HOST
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

    def onMessage(self, ws, evt):

        evt = json.loads(evt)
        if 0: # debug == 1: 
            #print(u'OKEX.onMessage_Everything:{}'.format(evt))
            print ('evt[0][channel]', evt)
            print ('type', type(evt))

            if (type(evt) is list ):
                print ('yes')
            else:
                print ('no')
        else : 
            try : 
                #print (evt)
                #print (evt[0]['channel'])
                if (type(evt) is list ):    # to get ride of ping/pong of the response pong as dictionary

                    if evt[0]['channel'] == 'ok_sub_futureusd_%s_ticker_quarter' % (Golbal_control.product_name_channel) :
                        self.data_ok_sub_futureusd_product_ticker_quarter = evt[0]['data']

                    if evt[0]['channel'] == 'ok_futureusd_orderinfo':
                        self.data_ok_futureusd_orderinfo = evt[0]['data']

                    if evt[0]['channel'] == 'ok_sub_futureusd_%s_trade_quarter' % (Golbal_control.product_name_channel):
                        self.data_ok_sub_futureusd_product_trade_quarter = evt[0]['data']

                    if evt[0]['channel'] == 'ok_sub_futureusd_%s_depth_quarter_10' % (Golbal_control.product_name_channel):
                        self.data_ok_sub_futureusd_product_depth_quarter_10 = evt[0]['data']

                    if evt[0]['channel'] == 'ok_sub_futureusd_%s_depth_quarter_20' % (Golbal_control.product_name_channel):
                        self.data_ok_sub_futureusd_product_depth_quarter_20 = evt[0]['data']

                    if evt[0]['channel'] == 'ok_sub_future_%s_depth_quarter_usd' % (Golbal_control.product_name_channel):
                        self.data_ok_sub_future_product_depth_quarter_usd = evt[0]['data']

                    if evt[0]['channel'] == 'ok_sub_futureusd_%s_index' % (Golbal_control.product_name_channel):
                        self.data_ok_sub_futureusd_product_index = evt[0]['data']

                    #################### Group of five ###
                    if evt[0]['channel'] == 'ok_sub_futureusd_trades':
                        self.data_ok_sub_futureusd_trades = evt[0]['data']

                    if evt[0]['channel'] == 'ok_sub_futureusd_positions':
                        self.data_ok_sub_futureusd_positions = evt[0]['data']

                    if evt[0]['channel'] == 'ok_sub_futureusd_userinfo':
                        self.data_ok_sub_futureusd_userinfo = evt[0]['data']

                    if evt[0]['channel'] == 'ok_futureusd_trade':
                        self.data_futureusd_trade = evt[0]['data']

                    if evt[0]['channel'] == 'ok_futureusd_cancel_order':
                        self.data_ok_futureusd_cancel_order = evt[0]['data']

                    ###################
                    if evt[0]['channel'] == 'ok_futureusd_userinfo':
                        self.data_ok_futureusd_userinfo = evt[0]['data']

                    if evt[0]['channel'] == '%s_forecast_price' % (Golbal_control.product_name_channel):
                        self.data_product_forecast_price = evt[0]['data']

                    if evt[0]['channel'] == 'login':
                        self.data_login = evt[0]['data']

                    if evt[0]['channel'] == 'addChannel':
                        self.data_addChannel = evt[0]['data']
            except:
                print ("API error")

    def onError(self, ws, evt):
        print(u'OKEX.onError_API:{}'.format(evt))
        Golbal_control.onError = 1     ### Alarm other threads that the connection has dropped

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
    # ----------------------------------------------------------------------
    def sendTradingRequest(self, channel, params):
        """发送交易请求"""
        # 在参数字典中加上api_key和签名字段
        params['api_key'] = self.apiKey
        params['sign'] = self.generateSign(params)
        # 生成请求
        d = {}
        d['event'] = 'addChannel'
        d['channel'] = channel
        d['parameters'] = params
        # 使用json打包并发送
        j = json.dumps(d)
        # 若触发异常则重连
        try:
            self.ws.send(j)
        except websocket.WebSocketConnectionClosedException as ex:
            print(u'OkexContractApi.sendTradingRequest exception:{},{}'.format(str(ex),traceback.format_exc()), file=sys.stderr)
        except Exception as ex:
            print(u'OkexContractApi.sendTradingRequest exception:{},{}'.format(str(ex), traceback.format_exc()), file=sys.stderr)
    # ----------------------------------------------------------------------
    def return_eos_ticker_quarter(self):
        return self.data_ok_sub_futureusd_eos_ticker_quarter

    def return_futureusd_orderinfo(self):
        return self.data_ok_futureusd_orderinfo

################## returns #############3
    def return_login(self):
        return self.data_login

    def return_addChannel(self):
        return self.data_addChannel

    def return_AllUnfinishedOrderInfo(self):
        return self.data_ok_futureusd_orderinfo

    def return_product_trade_quarter(self):
        return self.data_ok_sub_futureusd_product_trade_quarter 

    def return_product_depth_quarter_10 (self):
        return self.data_ok_sub_futureusd_product_depth_quarter_10

    def return_product_depth_quarter_20 (self):
        return self.data_ok_sub_futureusd_product_depth_quarter_20

    def return_futureusd_product_index(self):
        return self.data_ok_sub_futureusd_product_index

################### Group of Five ###############
    def return_ok_sub_futureusd_trades(self):
        return self.data_ok_sub_futureusd_trades

    def return_ok_sub_futureusd_positions(self):
        return self.data_ok_sub_futureusd_positions

    def return_ok_sub_futureusd_userinfo(self):
        return self.data_ok_sub_futureusd_userinfo 

    def return_futureusd_trade(self):
        return self.data_futureusd_trade

    def return_futureusd_cancel_order(self):
        return self.data_ok_futureusd_cancel_order

  ######################################################      

    def return_ok_futureusd_userinfo(self):
        return self.data_ok_futureusd_userinfo

    def return_product_forecast_price(self):
        return self.data_product_forecast_price 

########################################################################
class OKEXSpotApi(OKEXWebSocket):
    """OKEX Spot trade"""

    def __init__(self):
        """Constructor"""
        super(OKEXSpotApi, self).__init__()

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
        self.apiKey = ''  # 用户名
        self.secretKey = ''  # 密码
        self.ws = None  # websocket应用对象  期货对象
        self.active = False  # 还存活
        self.use_lever_rate = 20
        self.trace = False

        ############### Standard #########################
        self.data_login = []
        self.data_addChannel = []

        ###############api.futureOrderInfo( ##################3  api.futureAllUnfinishedOrderInfo(       It has to be run for multiple tries ###############
        self.data_ok_futureusd_orderinfo = []

        ###############api.subsribeFutureTicker( ###########
        self.data_ok_sub_futureusd_product_ticker_quarter = []

        ################api.subscribeFutureTrades(
        self.data_ok_sub_futureusd_product_trade_quarter = []

        ###############api.subscribeFutureDepth10()
        self.data_ok_sub_futureusd_product_depth_quarter_10 = []

        ###############api.subscribeFutureDepth20()
        self.data_ok_sub_futureusd_product_depth_quarter_20 = []

        ###############api.subscribeFutureDepth(
        self.data_ok_sub_future_product_depth_quarter_usd = []

        ##############api.subscribeFutureIndex(    and api.futureSubscribeIndex(  #####
        self.data_ok_sub_futureusd_product_index = []

        ############# Group of five for api.futureTrade(   api.futureCancelOrder( #############
        self.data_ok_sub_futureusd_trades = []
        self.data_ok_sub_futureusd_positions = []
        self.data_ok_sub_futureusd_userinfo = []
        self.data_futureusd_trade = []
        self.data_ok_futureusd_cancel_order = []

        #############api.futureUserInfo()    **********
        self.data_ok_futureusd_userinfo = []

        ################api.X_forecast_price(  ######
        self.data_product_forecast_price = []
        
    def ChannelFutureTicker(self, symbol, contract_type):
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

    def ChannelFutureDepth10(self, symbol, contract_type):
        req = "{'event':'addChannel','channel':'ok_sub_futureusd_%s_depth_%s_10'}" % (symbol, contract_type)
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

        #=========================
    def futureTrade(self, symbol_pair, contract_type, type_, price, amount, _match_price='0', _lever_rate=None):
        params = {}
        params['symbol'] = str(symbol_pair)
        params['contract_type'] = str(contract_type)
        params['price'] = str(price)
        params['amount'] = str(amount)
        params['type'] = type_  # 1:开多 2:开空 3:平多 4:平空
        params['match_price'] = _match_price  # 是否为对手价： 0:不是 1:是 当取值为1时,price无效

        if _lever_rate != None:
            params['lever_rate'] = _lever_rate
        else:
            params['lever_rate'] = str(self.use_lever_rate)
        channel = 'ok_futureusd_trade'

        self.sendTradingRequest(channel, params)

    def futureCancelOrder(self, symbol_pair, orderid, contract_type):
        """
        期货撤单指令
        :param symbol_pair: 合约对
        :param orderid: 委托单编号
        :param contract_type: 合约类型
        :return:
        """
        params = {}
        params['symbol'] = str(symbol_pair)
        params['order_id'] = str(orderid)
        params['contract_type'] = str(contract_type)
        channel = 'ok_futureusd_cancel_order'
        self.sendTradingRequest(channel, params)

    def futureOrderInfo(self, symbol_pair, order_id, contract_type): #     , status, current_page, page_length=50):
        """
        发出查询期货委托
        :param symbol_pair: 合约对
        :param order_id: 委托单编号
        :param contract_type: 合约类型
        :param status: 状态
        :param current_page:当前页
        :param page_length: 每页长度
        :return:
        """
        params = {}
        params['symbol'] = str(symbol_pair)
        params['order_id'] = str(order_id)
        params['contract_type'] = str(contract_type)

        channel = 'ok_futureusd_orderinfo'

        self.sendTradingRequest(channel, params)