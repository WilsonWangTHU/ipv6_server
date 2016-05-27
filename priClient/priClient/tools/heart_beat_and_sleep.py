import urllib2
import time
import sys
import subprocess
sys.path.append('/priClient/')

from priClient.utils.internetInfo import get_ivi_address


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
    print(data)
    break
    time.sleep(10)
