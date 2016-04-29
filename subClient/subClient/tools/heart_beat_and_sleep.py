import urllib2
import time
# from subClientHeartbeat import heart_beat_ipv6


'''
In this function, the host send url request to record data
in django database.
The localloop server will return the configuration setting
'''


# global settings
port_num = 8000
test = True

while(True):

    if test:
        path = '/sendHeart/test/'
    else:
        path = '/sendHeart/'

    req = urllib2.Request('http://127.0.0.1:' + str(port_num) + path)
    response = urllib2.urlopen(req)
    sleep_time = float(response.read()) / 10
    time.sleep(sleep_time)
