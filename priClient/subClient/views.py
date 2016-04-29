from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from net_data.models import client_info, wlan_configuration
import datetime


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
            client_object.last_active_time
        if delta_time.total_seconds() > configuration.dying_time * 60 \
                or delta_time.total_seconds() < 0:
            client_object.delete()

    return HttpResponse(str(configuration.refreshing_client_time))


def change_and_restart_wlan(request):

    return


def home(request):
    return render(request, 'home.html')


def receive_heart_beat(request):
    # it is the test function. return the data of the heart beat
    if request.method != 'POST':
        return HttpResponseNotAllowed('What are doing? No data?')
    try:
        mac_address = request.POST['mac_address']
        ipv6_addresses = request.POST['ipv6_addresses']
        global_ipv6_address = request.POST['global_ipv6_address']
        heart_beart_frequency = request.POST['heart_beart_frequency']
    except KeyError:
        return HttpResponseNotAllowed('Wrong format')

    # old faces or new one?
    try:
        client = client_info.objects.get(mac_address=mac_address)
        client.mac_address = mac_address
        client.ipv6_addresses = mac_address
        client.global_ipv6_address = global_ipv6_address
        client.heart_beart_frequency = heart_beart_frequency
        client.last_active_time = datetime.datetime.now()
    except client_info.DoesNotExist:
        client = client_info(mac_address=mac_address,
                             ipv6_addresses=ipv6_addresses,
                             global_ipv6_address=global_ipv6_address,
                             heart_beart_frequency=heart_beart_frequency)
    client.save()
    return HttpResponse('success')
