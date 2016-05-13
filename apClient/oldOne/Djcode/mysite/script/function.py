import subprocess
import hashlib
import uuid
import socket
import struct
import fcntl

def md5(t_str):
    m = hashlib.md5()
    m.update(t_str)
    return m.hexdigest()

def write_file(filename,string):
    output=open(filename,'w')
    output.write(string)
    output.close()

def read_file(filename):
    innput=open(filename,'r')
    all_text = innput.read()
    innput.close()
    return all_text

def send_message(cmd):
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (t_out,err)=p.communicate()
    out = t_out.split('\n')
    t = out[0]
    return t_out 

def get_mac():
    node = uuid.getnode()
    mac = uuid.UUID(int = node).hex[-12:]
    return mac

def get_ip(ethname):
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s',ethname[:15]))[20:24]) 
