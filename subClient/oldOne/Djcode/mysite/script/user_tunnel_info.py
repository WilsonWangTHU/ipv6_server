from function import *
import ConfigParser

tunnelconfig_file='/etc/tunnel_config/tunnel.conf'
SERVER_ADDR = '-u xlat:tub20141008 202.112.35.231:8080'
tunnel_prefix1='sudo /usr/bin/curl -d type=%r -d mac=%r '
tunnel_prefix2='sudo /usr/bin/curl -d type=%r -d username=%r -d password=%r -d mac=%r '
tunnel_prefix3='sudo /usr/bin/curl -d type=%r -d username=%r -d password=%r -d mac=%r -d newname=%r -d newpd=%r '
tunnel_prefix4='sudo /usr/bin/curl -d type=%r -d username=%r -d password=%r -d mac=%r -d tunnel_type=%r -d delay=%r -d flow_in=%r -d flow_out=%r -d ip4_local=%r '
tunnel_postfix1=SERVER_ADDR+'/raspberry/'
tunnel_postfix2=SERVER_ADDR+'/raspberry/ -o /etc/openvpn/key.tar.gz'

def tunnel_communicate_mac(mac,ctype):
    string = tunnel_prefix1+tunnel_postfix1
    cmd = string%(ctype,mac)
    result = send_message(cmd)
    return result

def tunnel_communicate_download():
    username = read_config('UserInfo','username')
    password = read_config('UserInfo','password')
    mac = read_config('UserInfo','mac')
    string = tunnel_prefix2+tunnel_postfix2
    cmd = string%("download",username,password,mac)
    result = send_message(cmd)
    result = cmd
    return result

def tunnel_communicate_name(ctype):
    username = read_config('UserInfo','username')
    password = read_config('UserInfo','password')
    mac = read_config('UserInfo','mac')
    string = tunnel_prefix2+tunnel_postfix1
    cmd = string%(ctype,username,password,mac)
    result = send_message(cmd)
    print result
    return result

def tunnel_communicate_name_changename(ctype,new_un,new_pd):
    username = read_config('UserInfo','username')
    password = read_config('UserInfo','password')
    mac = read_config('UserInfo','mac')
    string = tunnel_prefix3+tunnel_postfix1
    cmd = string%(ctype,username,password,mac,new_un,new_pd)
    result = send_message(cmd)
    print result
    return result

def tunnel_communicate_name_state(tunnel_type,delay,flow_in,flow_out,ip4_local):
    username = read_config('UserInfo','username')
    password = read_config('UserInfo','password')
    mac = read_config('UserInfo','mac')
    string = tunnel_prefix4+tunnel_postfix1
    cmd = string%('tustate',username,password,mac,tunnel_type,delay,flow_in,flow_out,ip4_local)
    result = send_message(cmd)
    #print result
    return cmd

def write_userinfo(mac):
    t0 = tunnel_communicate_mac(mac,'bind')
    ui = t0.split(',')
    error = int(ui[0])
    if error!=1 and error!=2:
        return 0
    cf = ConfigParser.ConfigParser()
    cf.read(tunnelconfig_file)
    cf.set('UserInfo','mac',mac)
    if error == 1:
        cf.set('UserInfo','username',ui[10])
        cf.set('UserInfo','password',md5(ui[10]))
    cf.set('TunnelInfo','server_ipv4',ui[1])
    cf.set('TunnelInfo','client_ipv4',ui[2])

    cf.set('TunnelInfo','ipv6_addr_netmask',ui[3].split('/')[1])
    cf.set('TunnelInfo','ivi_addr_netmask',ui[4].split('/')[1])
    cf.set('TunnelInfo','openvpn_interface_netmask',ui[5].split('/')[1])
    cf.set('TunnelInfo','ip_interface_server_netmask',ui[6].split('/')[1])
    cf.set('TunnelInfo','ip_interface_client_netmask',ui[7].split('/')[1])

    cf.set('TunnelInfo','ipv6_addr',ui[3].split('/')[0]+'1')
    cf.set('TunnelInfo','ivi_addr',ui[4].split('/')[0])
    cf.set('TunnelInfo','openvpn_interface',ui[5].split('/')[0])
    cf.set('TunnelInfo','ip_interface_server',ui[6].split('/')[0])
    cf.set('TunnelInfo','ip_interface_client',ui[7].split('/')[0])
    cf.set('TunnelInfo','ivi_addr_port',ui[12])
    cf.set('TunnelInfo','ivi4_addr',ui[11])
    

    cf.set('TunnelInfo','sitname',ui[8])
    cf.set('TunnelInfo','openvpn_common_name',ui[9])
     
    cf.set('State','if_login','1')

    cf.write(open(tunnelconfig_file,'w'))
    return 1

def reset_userinfo():   
    cf = ConfigParser.ConfigParser()
    cf.read(tunnelconfig_file)

    cf.set('State','if_login',0)
    cf.set('State','if_first_login',0)
    cf.set('State','if_register',0)
    cf.set('State','tunnel_type',0)

    cf.set('UserInfo','mac',0)
    cf.set('UserInfo','username',0)
    cf.set('UserInfo','password',0)
    cf.set('TunnelInfo','server_ipv4',0)
    cf.set('TunnelInfo','client_ipv4',0)

    cf.set('TunnelInfo','ipv6_addr_netmask',0)
    cf.set('TunnelInfo','ivi_addr_netmask',0)
    cf.set('TunnelInfo','openvpn_interface_netmask',0)
    cf.set('TunnelInfo','ip_interface_server_netmask',0)
    cf.set('TunnelInfo','ip_interface_client_netmask',0)

    cf.set('TunnelInfo','ipv6_addr',0)
    cf.set('TunnelInfo','ivi_addr',0)
    cf.set('TunnelInfo','ivi4_addr',0)
    cf.set('TunnelInfo','ivi_addr_port',0)
    cf.set('TunnelInfo','openvpn_interface',0)
    cf.set('TunnelInfo','ip_interface_server',0)
    cf.set('TunnelInfo','ip_interface_client',0)

    cf.set('TunnelInfo','sitname',0)
    cf.set('TunnelInfo','openvpn_common_name',0)

    cf.write(open(tunnelconfig_file,'w'))
    return 1

def change_auth(username,password):
    cf = ConfigParser.ConfigParser()
    cf.read(tunnelconfig_file)
    cf.set('UserInfo','username',username)
    cf.set('UserInfo','password',password)
    cf.write(open(tunnelconfig_file,'w'))
    return 1

def write_state(state,value):
    if state!='if_register' and state!='if_login' and state!='if_first_login' and state!='tunnel_type':
        return 0
    cf = ConfigParser.ConfigParser()
    cf.read(tunnelconfig_file)
    cf.set('State',state,value)
    cf.write(open(tunnelconfig_file,'w'))
    return 1

def write_mac():
    mac = get_mac()
    cf = ConfigParser.ConfigParser()
    cf.read(tunnelconfig_file)
    cf.set('UserInfo','mac',mac)
    cf.write(open(tunnelconfig_file,'w'))
    return 1

def write_v4glb(v4glb):
    cf = ConfigParser.ConfigParser()
    cf.read(tunnelconfig_file)
    cf.set('TunnelInfo','client_ipv4',v4glb)
    cf.write(open(tunnelconfig_file,'w'))
    return 1

def read_config(section,option):
    cf = ConfigParser.ConfigParser()
    cf.read(tunnelconfig_file)
    try:
        result = cf.get(section,option)
        if section == 'State':
            result = int(result)
        return result
    except ConfigParser.NoOptionError:
        return -1
    except ConfigParser.NoSectionError:
        return -1
