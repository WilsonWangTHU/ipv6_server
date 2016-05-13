import os
import datetime
from utils.internetInfo import get_mac_address


pid_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pid.txt')
if os.path.isfile(pid_file_path):
    file_read = open(pid_file_path)
    pid = file_read.readline()
    print(pid)
    file_read.close()
else:
    pid = str(datetime.datetime.now()) + get_mac_address('wlan0')
    file_read = open(pid_file_path, 'w')
    file_read.write(pid)
    file_read.close()
