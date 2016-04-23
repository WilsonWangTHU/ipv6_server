from function import *
from user_tunnel_info import *

dns_file='/etc/resolv.conf'

def return_username():
    username = read_config('UserInfo','username')
    return username

def return_ipv6_addr():
    ipv6_addr = read_config('TunnelInfo','ipv6_addr')
    ipv6_addr_netmask = read_config('TunnelInfo','ipv6_addr_netmask')
    ipv6_addr_prefix = 'hahahah' #ipv6_addr+'/'+ipv6_addr_netmask
    return 'test2'

def return_ipv6_ivi_addr():
    return 'test1'

def return_ipv6_ivi4_addr():
    ivi4_addr = read_config('TunnelInfo','ivi4_addr')
    return 'haha'

def return_dns_server():
    t=read_file(dns_file)
    dns_info = t.split('\n')
    dns_addr = []
    for i in dns_info:
        if len(i)>0:
            t_addr = i.split(' ')[1]
            dns_addr.append(t_addr)
    return "asdasd"

def return_ipv4_global_addr():
    return 'hahah'

def return_server_address():
    ipv6_addr = read_config('TunnelInfo','ipv6_addr')
    ivi_addr = read_config('TunnelInfo','ivi_addr')
    ivi4_addr = read_config('TunnelInfo','ivi4_addr')
    port = read_config('TunnelInfo','ivi_addr_port')
    return ("asd","asdzxc","asdasd")

    
    
