import urllib2
import time
# from subClientHeartbeat import heart_beat_ipv6


'''
In this function, the host send url request to record data
in django database.
The localloop server will return the configuration setting
'''


# global settings
port_num = 70 # todo, the port number might change!
test = False

while(True):

    if test:
        path = '/sendHeart/test/'
    else:
        path = '/sendHeart/'

    req = urllib2.Request('http://127.0.0.1:' + str(port_num) + path)
    response = urllib2.urlopen(req)
    print(response.read())
    break
    print(sleep_time)
    time.sleep(sleep_time)
