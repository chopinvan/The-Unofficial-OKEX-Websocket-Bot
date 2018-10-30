# The-Unofficial-OKEX-Websocket-Bot

OKEX is fairly popular amoung Asian countries. But it is less known in regions outside of it. 

OKEX has its official API documentation. But they do not have any sample code that usable. 
https://github.com/okcoin-okex/API-docs-OKEx.com

For quant traders, API connection through an exchange is important. This websocket API is unofficial.But it saves people's work on reading bad English documentation of the official one, plus no need to reinvent the wheels of just getting connections.  

For this version, the REST API is added. It runs as a seperate thread. Because in OKEX v1, checking current position balance is only available through REST API. Code is modified to suit this project
https://github.com/Harry-Lucas/okcoin_to_okex_request

https://github.com/bihanggit


Websocket API provides fastest data connection, and unlimited refreshing. It is the reason Both websocket and Rest API are integrated together to supplement each other functions. This project has a robust connection and error handling system that either Websocket or Rest get accedental drop in internet connection, the program automantically recovers the lost connection. No need for users to do anything. 

For obvious reasons, my own trading strategies are not included. This is the fundementals for everyone to jump into the quant tradings. 


Run Demo.py for results 
