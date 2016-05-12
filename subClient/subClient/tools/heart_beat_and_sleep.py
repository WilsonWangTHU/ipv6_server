import urllib2
import time
import sys
import subprocess
sys.path.append('/subClient/')

from subClient.utils.internetInfo import get_ivi_address


'''
In this function, the host send url request to record data
in django database.
The localloop server will return the configuration setting
'''


# global settings
port_num = 70  # todo, the port number might change!
test = False

while(True):

    if test:
        path = '/sendHeart/test/'
    else:
        path = '/sendHeart/'

    old_address = get_ivi_address('eth0')
    req = urllib2.Request('http://127.0.0.1:' + str(port_num) + path)
    response = urllib2.urlopen(req)
    data = response.read()
    isSuccess = (data.split('\n')[0] == 'success')

    if isSuccess:
        new_address = data.split('\n')[1]
        sleep_time = float(data.split('\n')[2])
        print(old_address)
        print(new_address)
        if old_address != new_address and old_address != 'None':
            subprocess.Popen('sudo ip -6 addr del ' + old_address + ' dev eth0', shell=True)
            subprocess.Popen('sudo ip -6 addr add ' + new_address + ' dev eth0', shell=True)
        else:
            subprocess.Popen('sudo ip -6 addr add ' + new_address + ' dev eth0', shell=True)
    else:
        if old_address != 'None':
            subprocess.Popen('sudo ip -6 addr del ' + old_address + ' dev eth0', shell=True)
            sleep_time = float(data.split('\n')[1])
    break
    print(data)
    time.sleep(sleep_time)
