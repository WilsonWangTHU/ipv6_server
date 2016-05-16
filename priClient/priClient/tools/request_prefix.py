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
port_num = 70 # todo, the port number might change!
test = False

def change_radvd_settings(address):
    gateway = address + '1'
    gateway = gateway.upper()  # radvd use uppercase
    process = subprocess.Popen('sudo cp /subClient/subClient/tools/radvd.template /subClient/subClient/tools/radvd.conf', shell=True)
    process.wait()

    process = subprocess.Popen('sudo sed -i "s/THEPREFIX/' + gateway + '/g" `grep THEPREFIX -rl /subClient/subClient/tools/radvd.conf`', shell=True)
    process.wait()
    process = subprocess.Popen('sudo cp /subClient/subClient/tools/radvd.conf /etc/', shell=True)
    process.wait()
    subprocess.Popen('sudo service radvd restart', shell=True)
    process = subprocess.Popen('sudo killall hostapd', shell=True)
    process.wait()
    subprocess.Popen('sudo hostapd -B /subClient/subClient/hostapd_conf/hostapd.conf', shell=True)

while(True):
    if test:
        path = '/send_prefix_request/test/'
    else:
        path = '/send_prefix_request/'

    req = urllib2.Request('http://127.0.0.1:' + str(port_num) + path)
    response = urllib2.urlopen(req)
    data = response.read()
    isSuccess = (data.split('\n')[0] == 'success')
    print(data)

    if isSuccess:
        new_address = data.split('\n')[1]
        if new_address == 'None':
            break
        sleep_time = float(data.split('\n')[2])
        subprocess.Popen('sudo ip -6 addr add ' + new_address + '1/64 dev wlan1', shell=True)
        
        # change the settings of apache2 is necessary
        change_radvd_settings(new_address)
    else:
        subprocess.Popen('sudo service radvd stop', shell=True)
    
    break
    print(data)
    time.sleep(sleep_time * 10)
