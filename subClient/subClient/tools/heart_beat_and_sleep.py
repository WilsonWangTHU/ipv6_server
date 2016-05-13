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


def change_apache2_settings(address):
    # the port number is calculated
    pos = address.find('::')
    apache_port_num = int(address[pos - 4: pos]) % 16 + 1024
    new_string = str(apache_port_num)
    process = subprocess.Popen('sudo cp /subClient/subClient/tools/apache2.template /subClient/subClient/tools/apache2.conf', shell=True)
    process.wait()
    print('sudo sed -i "s/FFFF/' + new_string + '/g" `grep FFFF -rl /subClient/subClient/tools/apache2.conf`')
    process = subprocess.Popen('sudo sed -i "s/FFFF/' + new_string + '/g" `grep FFFF -rl /subClient/subClient/tools/apache2.conf`', shell=True)
    process.wait()
    process = subprocess.Popen('sudo cp /subClient/subClient/tools/apache2.conf /etc/apache2/', shell=True)
    process.wait()
    subprocess.Popen('sudo service apache2 restart', shell=True)


while(True):
    if test:
        path = '/sendHeart/test/'
    else:
        path = '/sendHeart/'

    old_address = get_ivi_address('wlan0')
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
            subprocess.Popen('sudo ip -6 addr del ' + old_address + ' dev wlan0', shell=True)
            subprocess.Popen('sudo ip -6 addr add ' + new_address + ' dev wlan0', shell=True)
        else:
            subprocess.Popen('sudo ip -6 addr add ' + new_address + ' dev wlan0', shell=True)

        # change the settings of apache2 is necessary
        if old_address != new_address:
            change_apache2_settings(new_address)
    else:
        if old_address != 'None':
            subprocess.Popen('sudo ip -6 addr del ' + old_address + ' dev wlan0', shell=True)
            sleep_time = float(data.split('\n')[1])
    break
    print(data)
    time.sleep(sleep_time)
