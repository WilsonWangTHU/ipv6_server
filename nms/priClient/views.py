from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from net_data.models import client_info, wlan_configuration, ivi_address_pool
from net_data.util import create_client_info, delete_client_info, change_client_info, restart_wlan
import datetime
import IPy


def refresh_client_info(request=0):
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
                           ivi_address=ivi_address)
    except client_info.DoesNotExist:
        create_client_info(mac_address=mac_address,
                           ipv6_addresses=ipv6_addresses,
                           global_ipv6_address=global_ipv6_address,
                           heart_beat_frequency=heart_beat_frequency,
                           ivi_address=ivi_address)

    return HttpResponse('success\n')


def show_users(request, e=0):
    major_id = int(e)
    if major_id == 0:  # if no id is specified, show 1th
        major_id = 1

    post_list = client_info.objects.all()
    is_empty_list = (len(post_list) == 0)

    return render(request, 'user.html',
                  {'post_list': post_list,
                      'empty_list': is_empty_list,
                      'major_id': major_id,
                      'show_pi': post_list[major_id - 1],
                      'show_all_addresses':
                          post_list[major_id - 1].ipv6_addresses.all()}
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
