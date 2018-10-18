from okex_websocket import *
import time
from termcolor import colored

API = OKEXFuturesApi()


class ColorPrint:
    @staticmethod
    def print_fail(message, end = '\n'):
        sys.stderr.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + end)
    @staticmethod
    def print_pass(message, end = '\n'):
        sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)
    @staticmethod
    def print_warn(message, end = '\n'):
        sys.stderr.write('\x1b[1;33m' + message.strip() + '\x1b[0m' + end)
    @staticmethod
    def print_info(message, end = '\n'):
        sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)
    @staticmethod
    def print_bold(message, end = '\n'):
        sys.stdout.write('\x1b[1;37m' + message.strip() + '\x1b[0m' + end)

class CustomOrderManager(object):
    def current_positions(position_data):

        position_api_info = API.return_ok_sub_futureusd_trades()
        latest_position_feedback = API.return_futureusd_orderinfo()
        position_base_info = {"data": [position_api_info]}
        position_for_display = {"data": []}
        for i in range(0,len(position_data['data'])):
            if position_data['data'][i]['orderid'] != position_api_info['orderid']:
                position_base_info['data'].append(position_data['data'][i])
            if (type (latest_position_feedback) is dict) :
                for i in range(0,len(position_base_info['data'])):
                    if position_base_info['data'][i]['orderid'] == latest_position_feedback['orders'][0]['order_id']:
                        position_base_info['data'][i]['status'] = latest_position_feedback['orders'][0]['status']

        for i in range(0,len(position_base_info['data'])):
            if ((position_base_info['data'][i]['status'] == 0) or (position_base_info['data'][i]['status'] == 1)):
                position_for_display['data'].append(position_base_info['data'][i])
        return position_for_display

    def display_position( position_data_raw ):
        for i in range(0,len(position_data_raw['data'])):
            OrderID = position_data_raw['data'][i]['orderid']
            Amount = position_data_raw['data'][i]['amount']
            Order_Price = position_data_raw['data'][i]['price'] 
            Order_Type_init = position_data_raw['data'][i]['type']
            Filled_Amount = position_data_raw['data'][i]['deal_amount']
            Date = position_data_raw['data'][i]['create_date_str']
            if Order_Type_init == 1:
                Order_type = "Long"
                ColorPrint.print_pass("===================================================")
                print ("Order ID: ", Date , "Amount :",Amount, "Filled:", Filled_Amount, "Submit price : ",Order_Price, Order_type )
                ColorPrint.print_pass("===================================================")
                #print ("\n")
            elif Order_Type_init == 2:
                Order_type = "Short"
                ColorPrint.print_fail("===================================================")
                print ("Order ID: ", Date , "Amount :",Amount, "Filled:", Filled_Amount, "Submit price : ",Order_Price, Order_type )
                ColorPrint.print_fail("===================================================")
                #print ("\n")
            elif Order_Type_init == 3:
                Order_type = "Close Long"
                ColorPrint.print_fail("===================================================")
                print ("Order ID: ", Date , "Amount :",Amount, "Filled:", Filled_Amount, "Submit price : ",Order_Price, Order_type )
                ColorPrint.print_fail("===================================================")
                #print ("\n")
            elif Order_Type_init == 4:
                Order_type = "Close Short"
                ColorPrint.print_pass("===================================================")
                print ("Order ID: ", Date , "Amount :",Amount, "Filled:", Filled_Amount, "Submit price : ",Order_Price, Order_type )
                ColorPrint.print_pass("===================================================")
                #print ("\n")

    def display_pack(position_data):
        position_data = CustomOrderManager.current_positions(position_data)
        CustomOrderManager.display_position( position_data)
        return position_data         

    def Cancel_everything( position_data_raw ):
        for i in range(0,len(position_data_raw['data'])):
            OrderID = position_data_raw['data'][i]['orderid']
            CustomOrderManager.cancel_order(OrderID)

    def submit_order( order_type, order_price , amount ):
        # This function takes order price, and order types of " buy, buy_cover, short, short_cover", then returns the orderID that it submits
        # order_type : # 1: Buy 2:Short 3:Cover_buy 4: Cover_Short
        #api.futureTrade( product_name, "quarter" ,"1" , 2 , 1 , _match_price = '0' , _lever_rate = '1')  # 14245727693     ###### Tested
        API.futureTrade( Golbal_control.product_name, Golbal_control.product_delivery , order_type , order_price , amount , _match_price = '0' , _lever_rate = '1')  # 14245727693     ###### Tested
        sleep(1)
        test_buffer = API.return_ok_sub_futureusd_trades()
        if (type (test_buffer) is dict) : 
            return test_buffer['orderid'] 

    def cancel_order( orderid ):

        API.futureCancelOrder(Golbal_control.product_name,orderid, Golbal_control.product_delivery) 
        sleep(1)
        test_buffer = API.return_ok_sub_futureusd_trades()
        try:
            if (type (test_buffer) is dict) : 
                if (test_buffer['status'] == -1):
                    return test_buffer['status'] # -1 means successful
                else :
                    sleep(1)
                    API.futureCancelOrder(Golbal_control.product_name,orderid, Golbal_control.product_delivery)
                    sleep(1)
                    test_buffer_retry = API.return_ok_sub_futureusd_trades()
                    if (type (test_buffer) is dict) : #if (type(evt) is list )
                        if (test_buffer['status'] == -1):
                            return test_buffer['status'] # -1 means successful
                        else: return "cancel_order_error else"
        except : 
            sleep(1)
            API.futureCancelOrder(Golbal_control.product_name,orderid, Golbal_control.product_delivery) 
            sleep(1)
            test_buffer_retry = API.return_ok_sub_futureusd_trades()
            if (type (test_buffer) is dict) : #if (type(evt) is list )
                if (test_buffer['status'] == -1):
                    return test_buffer['status'] # -1 means successful
                else: return "cancel_order_error except"

