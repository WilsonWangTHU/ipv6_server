from django.shortcuts import render, render_to_response
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from mysite.tunnel_function import *
import time

def ifconfig(request):
    response=HttpResponse()
    response['Contene-Type']="text/javascript"
    error = iflogin()
    response.write(error)
    return response

def info(request):
    error = iflogin()
    if error==0:
        return render_to_response('first_login.html')
    error=iftunnel()
    info_tuple=return_tunnel_info()
    dns_len = len(info_tuple[2])
    return render_to_response('info_new.html',{'username':info_tuple[0],'v6_gate':info_tuple[1],'ivi_gate':info_tuple[2],'ivi4_gate':info_tuple[3],'dns_list':info_tuple[4],'v4_global':info_tuple[5],'server_addr':info_tuple[6][0],'server_ivi_addr':info_tuple[6][1],'server_ivi4_addr':info_tuple[6][2]})

def error(request):
    return render_to_response('error.html') 
