import urllib2
import time
# from subClientHeartbeat import heart_beat_ipv6


'''
In this function, the host send url request to record data
in django database.
The localloop server will return the configuration setting
'''


# global settings
port_num = 1037

while(True):
    try:
        req = urllib2.Request('http://127.0.0.1:' + str(port_num) + '/record/')
        response = urllib2.urlopen(req)
        print('A data is recorded')
        time.sleep(float(response.read()))
    except:
        print('error')
