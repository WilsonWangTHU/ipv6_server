from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from net_data.models import client_info, wlan_configuration, ivi_address_pool
from net_data.util import create_client_info, delete_client_info, change_client_info, restart_wlan
import datetime
import IPy
import subprocess
from itertools import chain
from netaddr.ip import IPNetwork

def refresh_client_info(request=0):
    # this function could be used by url request, or used by other
    # plain request
    debug_info = ''
    objects = client_info.objects.all()

    if len(objects) == 0:
        return HttpResponse('success')

    for client_object in objects:
        ipv6_address = client_object.global_ipv6_address
        print('now testing:ping6 -c 3 -i 0.2 ' + ipv6_address)
        if ipv6_address == 'None':
            client_object.life = 'Dead'
            client_object.save()
            continue

        get_ping_result = subprocess.Popen('ping6 -c 3 -i 0.2 ' + ipv6_address, shell=True, stdout=subprocess.PIPE)
        get_result = subprocess.Popen('grep transmitted', shell=True, stdout=subprocess.PIPE, stdin=get_ping_result.stdout)
        result = get_result.communicate()[0]
        debug_info = debug_info + result
        try:
            received_packets = result.split(' ')[3]
            if int(received_packets) < 1:
                client_object.life = 'Dead'
                client_object.save()
        except:
            client_object.life = 'Dead'
            client_object.save()
    return HttpResponse(debug_info)

def old_refresh_client_info(request=0):
    # this function could be used by url request, or used by other
    # plain request
    objects = client_info.objects.all()
    configuration = wlan_configuration.objects.all()
    if len(configuration) == 0:
        configuration = wlan_configuration()
        configuration.save()
    else:
        configuration = configuration[0]

    if len(objects) == 0:
        return HttpResponse(str(configuration.refreshing_client_time))

    for client_object in objects:
        delta_time = datetime.datetime.now() - \
            client_object.last_active_time.replace(tzinfo=None)
        if delta_time.total_seconds() > configuration.dying_time * 60 \
                or delta_time.total_seconds() < 0:
            delete_client_info(client_object)

    return HttpResponse(str(configuration.refreshing_client_time))


def change_and_restart_wlan(request=0):
    # TODO: the function of restart wlan
    restart_wlan()
    return


def change_settings(request):
    # TODO: ssl needed or admin needed
    data_config = wlan_configuration.objects.all()

    # are you first time here? then initialize the configuration
    if len(data_config) != 1:
        wlan_configuration.objects.all().delete()
        data_config = wlan_configuration()
    else:
        data_config = data_config[0]

    if request.method != 'POST':
        return render(request, 'show_settings.html',
                      {'settings': data_config})
    # the change
    if 'channel' in request.POST:
        if request.POST['channel'].isdigit() and request.POST['channel'] != '':
            data_config.channel = request.POST['channel']
    if 'password' in request.POST:
        if request.POST['password'].isdigit() and request.POST['password'] != '':
            data_config.password = request.POST['password']
    if 'dying_time' in request.POST:
        if request.POST['dying_time'].isdigit() and request.POST['dying_time'] != '':
            data_config.dying_time = request.POST['dying_time']
    if 'refreshing_client_time' in request.POST:
        if request.POST['refreshing_client_time'].isdigit() and request.POST['refreshing_client_time'] != '':
            data_config.refreshing_client_time = \
                request.POST['refreshing_client_time']

    data_config.save()

    return render(request, 'show_settings.html',
                  {'settings': data_config, 'Congrats': 'Successfully Changed The Settings'})


def show_settings(request):
    data_config = wlan_configuration.objects.all()

    # are you first time here? then initialize the configuration
    if len(data_config) != 1:
        wlan_configuration.objects.all().delete()
        data_config = wlan_configuration()
    else:
        data_config = data_config[0]

    return render(request, 'show_settings.html',
                  {'settings': data_config})


def home(request):
    return render(request, 'index.html')


def receive_heart_beat(request):
    # it is the test function. return the data of the heart beat
    if request.method != 'POST':
        return HttpResponse('What are doing? No data?')
    try:
        mac_address = request.POST['mac_address']
        ipv6_addresses = request.POST['ipv6_addresses']
        global_ipv6_address = request.POST['global_ipv6_address']
        heart_beat_frequency = request.POST['heart_beat_frequency']
        ivi_address = request.POST['ivi_address']
        position = request.POST['position']
        prefix = request.POST['prefix']
    except KeyError:
        return HttpResponseNotAllowed('Wrong format')

    # old faces or new one?
    try:
        client = client_info.objects.get(mac_address=mac_address)
        change_client_info(client,
                           mac_address=mac_address,
                           ipv6_addresses=ipv6_addresses,
                           global_ipv6_address=global_ipv6_address,
                           heart_beat_frequency=heart_beat_frequency,
                           ivi_address=ivi_address,
                           prefix=prefix,
                           position=position)
    except client_info.DoesNotExist:
        create_client_info(mac_address=mac_address,
                           ipv6_addresses=ipv6_addresses,
                           global_ipv6_address=global_ipv6_address,
                           heart_beat_frequency=heart_beat_frequency,
                           ivi_address=ivi_address,
                           prefix=prefix,
                           position=position)

    return HttpResponse('success\n')


def show_users(request, e=0):
    major_id = int(e)
    if major_id == 0:  # if no id is specified, show 1th
        major_id = 1

    # get the AP, APClient, Client in order
    APClient = client_info.objects.filter(position='Client/AP')
    AP = client_info.objects.filter(position='AP')
    Client = client_info.objects.filter(position='Client')
    post_list = list(chain(AP, APClient, Client))

    is_empty_list = (len(post_list) == 0)

    # calculate the curresponding IVI address
    ivi_ipv6_address = post_list[major_id - 1].ivi_address
    if ivi_ipv6_address.find('::/96') == -1:
        ivi_ipv4_address = 'None'
    else:
        pos = ivi_ipv6_address.find('::')
        apache_port_num = int(ivi_ipv6_address[pos - 4: pos]) % 16 + 1024
        ivi_ipv4_address = '121.194.168.143:' + str(apache_port_num) + '/home/'

    # calculate the connected users
    show_pi = post_list[major_id - 1]
    show_sons = []
    show_son_id = []
    id_counter = 0
    show_parents = []
    if show_pi.position.find('AP') != -1:
        # get who is connected to it!
        the_prefix = show_pi.prefix
        for pis in post_list:
            pis_prefix = str(IPNetwork(pis.global_ipv6_address + '/64').network)
            if pis_prefix == the_prefix:
                show_sons.append("<a href='/users/" + str(id_counter + 1) + "'>" + str(pis.global_ipv6_address) + '</a>')
            id_counter = id_counter + 1

    id_counter = 0
    if show_pi.position.find('Client') != -1:
        # who is your daddy?
        # I am your father!
        pis_prefix = str(IPNetwork(show_pi.global_ipv6_address + '/64').network)
        for pis in post_list:
            the_prefix = pis.prefix
            if pis_prefix == the_prefix:
                show_parents.append("<a href='/users/" + str(id_counter + 1) + "'>" + str(pis.global_ipv6_address) + '</a>')
            id_counter = id_counter + 1
    
    if len(show_parents) == 0:
        show_parents.append('None')


    return render(request, 'user.html',
                  {'post_list': post_list,
                      'empty_list': is_empty_list,
                      'major_id': major_id,
                      'show_pi': post_list[major_id - 1],
                      'show_all_addresses':
                          post_list[major_id - 1].ipv6_addresses.all(),
                      'ivi_ipv4_address': ivi_ipv4_address,
                      'show_sons': show_sons,
                      'show_parents': str(show_parents[0])}
                  )


def about(request):
    return render(request, 'info.html')


def ivi_address(request):
    addresses = ivi_address_pool.objects.all()

    # are you first time here? then initialize the configuration
    if len(addresses) == 0:
        return render(request, 'ivi.html', {'address': '', 'num': 0})
    else:
        return render(request, 'ivi.html', {'address': addresses, 'num': 1})


def change_ivi(request):
    # TODO: ssl needed or admin needed
    if request.method != 'POST':
        return ivi_address(request)

    congrat_info = 'Invalid input, check again!'

    if 'status' in request.POST and 'iviaddress' in request.POST:  # change the status
        if request.POST['status'].isdigit() and 0 < int(request.POST['status']) <= 2:
            objects = ivi_address_pool.objects.filter(address=request.POST['iviaddress'])
            if len(objects) != 0:
                objects[0].status = int(request.POST['status'])
                objects[0].save()
                congrat_info = 'Successfully Changed The Settings'
    else:
        if 'newiviaddress' in request.POST:
            std_ivi_address = IPy.IP(request.POST['newiviaddress'].split('/')[0]).strCompressed() + '/' + request.POST['newiviaddress'].split('/')[1]
            new_obj = ivi_address_pool(address=std_ivi_address)
            new_obj.save()
            congrat_info = 'Successfully Changed The Settings'
        if 'deadiviaddress' in request.POST:
            objects = ivi_address_pool.objects.filter(address=request.POST['deadiviaddress'])
            if len(objects) != 0:
                objects[0].delete()
                congrat_info = 'Successfully Changed The Settings'

    addresses = ivi_address_pool.objects.all()

    # are you first time here? then initialize the configuration
    if len(addresses) == 0:
        return render(request, 'ivi.html', {'address': '', 'num': 0, 'Congrats': congrat_info})
    else:
        return render(request, 'ivi.html', {'address': addresses, 'num': 1, 'Congrats': congrat_info})
