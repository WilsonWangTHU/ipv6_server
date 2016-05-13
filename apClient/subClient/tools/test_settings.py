import urllib2, urllib
import time
# from subClientHeartbeat import heart_beat_ipv6


'''
In this function, the host send url request to record data
in django database.
The localloop server will return the configuration setting
'''


# global settings
port_num = 8000

settings = {'sample_period': 42, 'sample_volumn': 10, 'heart_beat_period': 42}
settings = urllib.urlencode(settings)
req = urllib2.Request('http://127.0.0.1:' + str(port_num) + '/settings/', data=settings)
response = urllib2.urlopen(req)
print(response.readlines())
