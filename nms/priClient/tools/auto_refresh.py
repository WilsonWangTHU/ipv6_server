# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 20:46:36 2016

@author: wtw
"""
import urllib2
import time

'''
In this function, the host send url request to refresh the list of users in
the server The local link. Server will return the configuration setting
'''


# global settings
port_num = 70
test = True

while(True):
    path = '/auto_refresh/'

    req = urllib2.Request('http://127.0.0.1:' + str(port_num) + path)
    response = urllib2.urlopen(req)
    data = response.read()
    print(data)

    break
    time.sleep(sleep_time)
