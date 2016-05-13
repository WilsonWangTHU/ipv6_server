from function import *
from user_tunnel_info import *

def ping_test():
    t_cmd = "sudo ping6 -c 3 ipv6.google.com"
    flag=0
    i=-1
    while(i<3):
        i+=1 
        login_flag=read_config('State','if_login')
        if login_flag==0:
            continue
        ipv6_addr = read_config('TunnelInfo','ipv6_addr')
        cmd = t_cmd+" -I "+ipv6_addr
        t_out = send_message(cmd)
        out = t_out.split('\n')
        nn = out[0]
        if len(out)>=7:
            n4 = out[6]
            out1 = n4.split(',')
            if(len(out1)<2):
                continue
            out2 = out1[1]
            out3 = out2[1]
            t = len(out[1])
            if out3 != '0':
                #print 1
                return 1
    return 0

