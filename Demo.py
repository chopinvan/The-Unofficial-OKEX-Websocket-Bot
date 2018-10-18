
from listener_websocket import *
from Position_holding_RestAPI import *





def display_current_order(): #This is the infenstructure for the display thread.  Everything to put on screen should be in this thread for central management
    sleep(5)  # to wait till API.return_ok_sub_futureusd_trades() finally get some data in the list
    
    Golbal_control.position_data['data'].append(API.return_ok_sub_futureusd_trades())

    
    while 1 :
        if 0:  # debug mode on
            #print ("position_datadebug ",  position_data)
            print (API.return_ok_sub_futureusd_trades())
            sleep(0.01)

        else:

            if Golbal_control.kill:
                Golbal_control.kill = False
                return
            if Golbal_control.position_reset:
                Golbal_control.position_data = {'data': []}
                Golbal_control.position_reset = 0
            else:
                Golbal_control.position_data = CustomOrderManager.display_pack(Golbal_control.position_data) 

                print ("position_data debug ",  Golbal_control.position_data) 
                print ("Program is running alive. Current parameters of buy and sell amount is: Sell %s Buy %s"  % (Golbal_control.sell_amount, Golbal_control.buy_amount) )
                

                print ("Current_long_position", Golbal_control.Current_long_position)
                print ("Current_short_position", Golbal_control.Current_short_position)

                print ("Current_resting_position_long", Golbal_control.Current_resting_position_long)
                print ("Current_resting_position_short", Golbal_control.Current_resting_position_short)

                print ("Current_long_position_entry_price", Golbal_control.Current_long_position_entry_price)
                print ("Current_short_position_entry_price", Golbal_control.Current_short_position_entry_price)

                print ("Current_long_position_profit", Golbal_control.Current_long_position_profit)
                print ("Current_short_position_profit", Golbal_control.Current_short_position_profit)

                #### check stale orders ###
                
                order_list_to_display = len(Golbal_control.position_data['data'])
                if (order_list_to_display > 0 ):
                    print ("Length debug###########",order_list_to_display )
                    OrderID_Stale_check = Golbal_control.position_data['data'][order_list_to_display -1]['orderid']
                    print ("OrderID *****",OrderID_Stale_check )
                    API.futureOrderInfo(Golbal_control.product_name,OrderID_Stale_check, Golbal_control.product_delivery)
                    print ("my own Order Status", Golbal_control.position_data['data'][order_list_to_display -1]['status'])
                    real_return = API.return_futureusd_orderinfo()
                    if (type (real_return) is dict) :

                        print ("Real return", real_return['orders'][0]['order_id'])
                        print ("Real return", real_return['orders'][0]['status'])

            if Golbal_control.cancel:
                CustomOrderManager.Cancel_everything(position_cancel_ready)
                Golbal_control.cancel = 0
                Golbal_control.position_reset = 1

            sleep (Golbal_control.Websocket_freq)    
            print(chr(27) + "[2J")              # black screen 


def sanity_check():
    sanity_check_flag = 0
    API.ChannelFutureDepth10(Golbal_control.product_name_channel,Golbal_control.product_delivery)    
    API.ChannelFutureIndex(Golbal_control.product_name_channel)        
    API.futureUserInfo()
    API.futureChannelIndex(Golbal_control.product_name_channel)
    print("api.return_login() :", API.return_login())
    test_order_id = CustomOrderManager.submit_order( 1,Golbal_control.sanity_check_input_price,1 ) 
    sleep(1)
    CustomOrderManager.cancel_order(test_order_id)
    sleep(1)
    if (  (API.return_ok_sub_futureusd_positions()['positions'][0]['bondfreez']) == 0 ):
        sanity_check_flag = 1
    return sanity_check_flag


def API_Connect_forever(): #This is the infenstructure for the API to remain connected thread.
    apiKey = Golbal_control.apiKey_websocket
    secretKey = Golbal_control.secretKey_websocket
    API.connect(apiKey, secretKey, True)
    sleep(3)
    API.login()
    sanity_check()
    while 1:
        API.sendHeartBeat()
        sleep (Golbal_control.sendHeartBeat)
        if Golbal_control.onError:
            API.reconnect()
            sleep(3)
            API.login()
            sanity_check()


def Positions_REST_API():

    while 1:

        AccountBalanceManager.current_holding_info()
        time.sleep(Golbal_control.REST_freq)



thread_API_Connect_forever = Thread(target=API_Connect_forever)
thread_API_Connect_forever.start()

thread_control_and_display = Thread(target=display_current_order)
thread_control_and_display.start()

thread_REST_connection = Thread(target=Positions_REST_API)
thread_REST_connection.start()