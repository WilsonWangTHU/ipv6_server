#!/usr/bin/python
import os
from sys import path
path.append(r"/home/wtw/Djcode/mysite/script")
import time
from function import *
from user_tunnel_info import *
from tunnel_local_manage import *
from read_tunnel_info import *
import ping_test

def iflogin():
    result = read_config('State','if_login')
    error = result
    return error

def iftunnel():
    result = read_config('State','tunnel_type')
    return result

def return_username():
    result = read_config('UserInfo','username')
    return result

def return_tunnel_info():
    username = return_username()
    ipv6_addr = return_ipv6_addr()
    ivi_addr = return_ipv6_ivi_addr()
    ivi4_addr = return_ipv6_ivi4_addr()
    dns_info = return_dns_server()
    ipv4_global_addr = return_ipv4_global_addr()
    server_addr = return_server_address()
    return (username,ipv6_addr,ivi_addr,ivi4_addr,dns_info,ipv4_global_addr,server_addr)

def quit_login(t):
    delete_tunnel_A()
    delete_tunnel_C()
    if t==1:
        tunnel_communicate_name('relbd')
    reset_userinfo()
    os.system("sudo /home/wtw/Djcode/mysite/script/logout_change_file")
    #os.system("sudo service apache2 graceful")
    #os.system("(sudo /project/Djcode/mysite/script/sleep & >> /dev/null)")
    #error2 = send_message("sudo service apache2 start")
    #write_file('/tmp/error.txt','1:'+str(error1)+'/n2:'+str(error2))
        
def iftong():
    flag = read_config('State','if_first_login')
    if flag==1:
        return 1
    else:
        return 0

def iftong2():
    flag = read_config('State','if_login')
    if flag==1:
        return 1
    else:
        return 0

def change_name(un_old,pd_old,un_new,pd_new):
    un_new = str(un_new)
    pd_new = md5(str(pd_new))
    un_old = str(un_old)
    pd_old = md5(str(pd_old))
    un_now = read_config('UserInfo','username')
    pd_now = read_config('UserInfo','password')
    if un_now!=un_old or pd_now!=pd_old:
        return 0
    error = tunnel_communicate_name_changename('cn',un_new,pd_new)
    if error == '1':
        change_auth(un_new,pd_new)
        return 1
    if error == '3':
        return 3
    return -1

def user_auth(username,password):
    pd = md5(str(password))
    change_auth(str(username),pd)
    error = tunnel_communicate_name('auth')
    return int(error)

def first_config_tunnel():
    os.system("sudo /home/wtw/Djcode/mysite/script/network_config.shell &")

def userlogin(resquest):
    t_username = resquest.POST.get('username','')
    t_password = resquest.POST.get('password','')
    pd = md5(t_password)
    result = write_userinfo(str(t_username),pd)
    if result==0:
        return 0
    #t_flag = tunnel_communicate_if_exsit(str(t_username),pd)
    #flag = int(t_flag)
    #if flag!=1:
    #    reset_userinfo()
    return 1

def tunnel_con1():
    login_flag = read_config('State','if_login')
    if login_flag==0:
        return 0
    tunnel_type = read_config('State','tunnel_type')
    if tunnel_type!=0:
        return 0 

    error = write_tunnel_A()
    if error == -1:
        return -1
    create_tunnel_A()
    time.sleep(5)
    error = ping_test.ping_test()
    if error==1:
        return 1
    delete_tunnel_A()
    return 0

def tunnel_con2():
    login_flag = read_config('State','if_login')
    if login_flag==0:
        return 0
    tunnel_type = read_config('State','tunnel_type')
    if tunnel_type!=0:
        return 0 
    error = write_tunnel_C()
    if error == -1:
        return -1
    create_tunnel_C()
    time.sleep(10)
    error = ping_test.ping_test()
    if error==1:
        return 2
    delete_tunnel_C()
    return 0

def tunnel_con3():
    login_flag = read_config('State','if_login')
    if login_flag==0:
        return 0
    tunnel_type = read_config('State','tunnel_type')
    if tunnel_type!=0:
        return 0 
    error = write_tunnel_A()
    if error == -1:
        return -1
    create_tunnel_A()
    error = ping_test.ping_test()
    if error==1:
        return 1
    delete_tunnel_A()
    error = write_tunnel_C()
    if error == -1:
        return -1
    create_tunnel_C()
    time.sleep(10)
    error = ping_test.ping_test()
    if error==1:
        return 2
    delete_tunnel_C()
    return 0

def del_tunnel():
    login_flag = read_config('State','if_login')
    if login_flag==0:
        return -1
    tunnel_type = read_config('State','tunnel_type')
    if tunnel_type==0:
        return  0
    if tunnel_type == 1:
        error = delete_tunnel_A()
        return error
    if tunnel_type == 2:
        error = delete_tunnel_C()
        return error*2
    return -1


def check_mac():
    mac = get_mac()
    error = write_userinfo(mac)
    return error    

def check_mac_state():
    mac = get_mac()
    t0 = tunnel_communicate_mac(mac,'bdstate')
    ui = t0.split(',')
    error = int(ui[0])
    return error

def change_bind(username,passwd):
    write_mac()
    mac=get_mac()
    change_auth(username,md5(passwd))
    t0 = tunnel_communicate_name('chbd')
    ui = t0.split(',')
    error = int(ui[0])
    if error == 0:
        return 0
    if error == 1:
        write_userinfo(mac)
	change_auth(username,md5(passwd))
        return 1
     
