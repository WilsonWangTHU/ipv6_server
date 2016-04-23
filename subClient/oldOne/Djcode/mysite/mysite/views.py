from django.shortcuts import render,render_to_response
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from mysite.tunnel_function import *

def test(request):
    return render_to_response('test.html')

def mac_error(request):
    return render_to_response('mac_error.html')

def guide_zero(request):
    login_flag=iflogin()
    if login_flag==1:
        return render_to_response('jump.html',{'jump_kind':1,'error':2,'next':'/'})
    return render_to_response('guide_page.html',{'page':0,'next':'/guide_page/0.5'})

def guide_half(request):
    login_flag=iflogin()
    if login_flag==1:
        return render_to_response('jump.html',{'jump_kind':1,'error':2,'next':'/'})
    error = check_mac_state() 
    next_page='#'
    next_page1='#'
    if error == 0:
        next_page = '/mac_error/'
    if error == 1:
        next_page = '/guide_page/1/1/'
        next_page1 = '/guide_page/1/2/'
    if error == 2:
        next_page = '/guide_page/1/1/'
    return render_to_response('guide_page.html',{'page':0.5,'error':error,'next':next_page,'next1':next_page1})
    

def guide_one_one(request):
    login_flag=iflogin()
    if login_flag==1:
        return render_to_response('jump.html',{'jump_kind':1,'error':2,'next':'/'})
    error = check_mac()
    next_page='#'
    username = ''
    if error == 0:
        next_page = '/mac_error/'
    if error == 2:
        next_page = '/guide_page/2/2/'
    if error == 1:
        username = return_username()
        next_page = '/guide_page/2/1/'
    return render_to_response('guide_page.html',{'page':1,'error':error,'username':username,'next':next_page})

def guide_one_two(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    if username == None or username == '' or password == None or password == '':    
        return render_to_response('guide_page.html',{'page':2,'error':0,'next':'/'})
    error = change_bind(username,password)
    next_page='#'
    if error == 1:
        next_page = '/guide_page/2/1/'
    if error == 0:
        next_page = '/'
    return render_to_response('guide_page.html',{'page':1,'username':username,'error':error,'next':next_page}) 
    

def guide_two_one(request):
    error=1
    next_page='#'
    if error == 1:
        next_page = '/first_config'
    if error == 0:
        next_page = '/'
    return render_to_response('guide_page.html',{'page':2,'error':error,'next':next_page})


def guide_two_two(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    if username == None or username == '' or password == None or password == '':    
        return render_to_response('guide_page.html',{'page':2,'error':0,'next':'/'})
    error = user_auth(username,password)
    next_page='#'
    if error == 1:
        next_page = '/first_config'
    if error == 0:
        next_page = '/'
    return render_to_response('guide_page.html',{'page':2,'error':error,'next':next_page})

def userauth(request):
    login_flag=iflogin()
    if login_flag==0:
        return render_to_response('jump.html',{'jump_kind':0,'next':'/guide_page/0'})
    return render_to_response('guide_page.html',{'page':1,'error':2,'next':'/userauth/result/'})
 
    
def first_config(request):
    error = iftong()
    if error == 1:
        return render_to_response('jump.html',{'jump_kind':1,'error':0,'next':'/'})
    first_config_tunnel()
    return render_to_response('first_login.html')


def info(request):
    error = iflogin()
    if error==0:
        return render_to_response('jump.html',{'jump_kind':0,'next':'/guide_page/0'})
    if error!=1:
        return render_to_response('jump.html',{'jump_kind':-1,'next':'/login'})
    error=iftunnel()
    info_tuple=return_tunnel_info()
    dns_len = len(info_tuple[2])
    return render_to_response('info.html',{'tunnel_type':error,'v6_net':info_tuple[0][0],'v6_gate':info_tuple[0][1],'ivi_net':info_tuple[1][0],'ivi_gate':info_tuple[1][1],'dns_list':info_tuple[2],'v4_global':info_tuple[3],'server_addr':info_tuple[4][0],'server_ivi_addr':info_tuple[4][1]})

def ifconfig(response):
    response=HttpResponse()
    response['Contene-Type']="text/javascript"
    error = iftong()
    response.write(error)
    return response

def changename(request):
    return render_to_response('changename.html')

def cnsubmit(request):
    un_old = request.POST.get('old_username','') 
    pd_old = request.POST.get('old_password','')
    un_new = request.POST.get('new_username','')
    pd_new = request.POST.get('new_password','')
    pd_new_again = request.POST.get('new_password_again','')
    if pd_new != pd_new_again:
        return render_to_response('jump.html',{'jump_kind':5,'next':'/','error':2})
    error = change_name(un_old,pd_old,un_new,pd_new)
    return render_to_response('jump.html',{'jump_kind':5,'next':'/','error':error})
    
        


def logout1(request):
    error = quit_login(0)
    return render_to_response('jump.html',{'jump_kind':4,'next':'/guide_page/0','error':error})

def logout2(request):
    error = quit_login(1)
    return render_to_response('jump.html',{'jump_kind':4,'next':'/guide_page/0','error':error})

def choose_tunnel(request):
    error = iflogin()
    if error==0:
        return render_to_response('jump.html',{'jump_kind':0,'next':'/guide_page/0'})
    error = iftunnel()
    t = request.POST.get('type','')
    tunnel_type = int(t)
    if error != 0:
        return render_to_response('jump.html',{'jump_kind':2,'next':'/','error':3})
    error=-1
    if tunnel_type==1:
        error = tunnel_con1()
    if tunnel_type == 2:
        error = tunnel_con2()
    if tunnel_type == 3:
        error = tunnel_con3()
    return render_to_response('jump.html',{'jump_kind':2,'next':'/','error':error})

def delete_tunnel(request):
    error = iflogin()
    if error==0:
        return render_to_response('jump.html',{'jump_kind':0,'next':'/guide_page/0'})
    error = del_tunnel()
    return render_to_response('jump.html',{'jump_kind':3,'next':'/','error':error})
    

