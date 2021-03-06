
#! /usr/bin/python
# -*-coding=utf-8 -*-

from urllib.request import urlopen
from urllib.parse import urlencode

import hashlib
import time
import json

def post(server_url, params):
    """
    data = urllib.urlencode(params)
    request = urllib2.Request(server_url, data)
    return json.loads(urllib2.urlopen(request, timeout=10).read())
    """
    """
    from urllib.request import urlopen
    from urllib.parse import urlencode
    url = "http://192.168.40.129:8080/cgi-bin/newtest1.py"
    params = urlencode({"personName":"tomjao","personAge":52,"personSex":"Fax"}).encode('utf-8')
    reply = urlopen(url,params).read()
    print(reply.decode("utf-8"))
    """
    params = urlencode(params).encode('utf-8')
    reply = urlopen(server_url,params).read()
    return reply

def getFacesList(server_url, params):
    #print(post(server_url, params).decode("utf-8"))
    result = post(server_url, params).decode("utf-8")
    ret = json.loads(result)
    print(ret)


if __name__ == "__main__":

   url = "http://192.168.1.219/v0.13/facemng/getFacesList?"
    
   timestamp = int(time.time())
   clientId = 33
   #clientSecret = "abc123"
   clientSecret = "1234567890"

   params = {"client_id":clientId, "client_secret":clientSecret,"timestamp":timestamp}

   paramNamesForSignature = sorted(["client_secret","client_id","timestamp"],key=str.lower)
   #print(paramNamesForSignature)
   paramValuesStr = ""
   for index in range(0, len(paramNamesForSignature)):
       param = paramNamesForSignature[index]
       paramValuesStr += str(params[param])

   #print(paramValuesStr)

   m = hashlib.md5()
   m.update(paramValuesStr.encode("utf-8"))
   signatureStr=m.hexdigest()
   #print(signatureStr)

   params["signature"]=signatureStr

   for key in params:
       url +="%s=%s&" % (key, params[key]) 

   print(url)
   params = {}
   getFacesList(url, params)

