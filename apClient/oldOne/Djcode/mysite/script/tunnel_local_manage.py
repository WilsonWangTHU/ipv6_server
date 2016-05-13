from function import *
from user_tunnel_info import *
import os



def config_tunnel_A():
    ipv4_s = read_config('TunnelInfo','server_ipv4')
    ipv4_c = read_config('TunnelInfo','client_ipv4')
    ipv6_c = read_config('TunnelInfo','ip_interface_client')+'/'+read_config('TunnelInfo','ip_interface_client_netmask')
    cmd_list=[]
    cmd_list.append("sudo ip tunnel add sitCernet64 mode sit ttl 128 remote %s local %s"%(ipv4_s,ipv4_c))
    cmd_list.append("sudo ip link set sitCernet64 up")
    cmd_list.append("sudo ip -6 route add ::/0 dev sitCernet64 metric 1")
    cmd_list.append("sudo ip -6 addr add %s dev sitCernet64"%ipv6_c)
    i=0
    while i<4:
        #send_message(cmd_list[i])
        result = os.system(cmd_list[i])
        i+=1

def delete_tunnel_A():
    login_flag = read_config('State','if_login')
    if login_flag==0:
        return 0
    tunnel_type = read_config('State','tunnel_type')
    if tunnel_type!=1:
        return 0
    tunnel_communicate_name('dA')
    cmd = "sudo ip tunnel del sitCernet64"
    os.system(cmd)
    write_state('tunnel_type','0')
    return 1   

def write_tunnel_A():
    login_flag = read_config('State','if_login')
    if login_flag==0:
        return 0 
    tunnel_type = read_config('State','tunnel_type')
    if tunnel_type!=0:
        return 0
    error = tunnel_communicate_name('cA')
    if error == '0':
        return -1
    write_state('tunnel_type','1')
    return 1

def write_tunnel_C():
    login_flag = read_config('State','if_login')
    if login_flag==0:
        return 0 
    tunnel_type = read_config('State','tunnel_type')
    if tunnel_type!=0:
        return 0
    error = tunnel_communicate_name('cC')
    if error == '0':
        return -1
    write_state('tunnel_type','2')
    return 1
 
def create_tunnel_A():
    login_flag = read_config('State','if_login')
    if login_flag==0:
        return 0 
    tunnel_type = read_config('State','tunnel_type')
    if tunnel_type!=1:
        return 0
    config_tunnel_A()
    
    
def create_tunnel_C():
    login_flag = read_config('State','if_login')
    if login_flag==0:
        return 0
    tunnel_type = read_config('State','tunnel_type')
    if tunnel_type!=2:
        return 0
    cmd = "sudo service openvpn start"
    os.system(cmd)
    return 1

def delete_tunnel_C():
    login_flag = read_config('State','if_login')
    if login_flag==0:
        return 0
    tunnel_type = read_config('State','tunnel_type')
    if tunnel_type!=2:
        return 0
    tunnel_communicate_name('dC')
    cmd = "sudo service openvpn stop"
    os.system(cmd)
    write_state('tunnel_type','0')
    return 1    
