#!/usr/bin/python
# -*- coding: utf-8 -*-

import http.client
import urllib
import json
import hashlib
import time
from retrying import retry

def buildMySign(params,secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    data = sign+'secret_key='+secretKey
    return  hashlib.md5(data.encode("utf8")).hexdigest().upper()


@retry(wait_fixed=500)   # wait 0.5 s for reconnection if ever drops
def httpGet(url,resource,params=''):
    conn = http.client.HTTPSConnection(url, timeout=1)
    conn.request("GET",resource  + params)
    try : 
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        #params.clear()
        #conn.close()
        return data

    except :
        raise IOError("Broken sauce, everything is hosed!!!111one")
        print ("httpGet error in my MD5, retrying ")

    


@retry(wait_fixed=500)   # wait 0.5 s for reconnection if ever drops
def httpPost(url,resource,params):
    headers = {
           "Content-type" : "application/x-www-form-urlencoded",
    }
    conn = http.client.HTTPSConnection(url, timeout=0.5)
    temp_params = urllib.parse.urlencode(params)
    conn.request("POST", resource, temp_params, headers)
    try : 
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        params.clear()
        conn.close()
        return data

    except :
        print ("httpPost error in my MD5, retrying ")
        raise IOError("Broken sauce, everything is hosed!!!111one")
        
        params.clear()
        conn.close()

    



        
     
