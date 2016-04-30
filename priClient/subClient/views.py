from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from net_data.models import client_info, wlan_configuration
from net_data.util import create_client_info, delete_client_info, change_client_info
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
            delete_client_info(client_object)
            # client_object.delete()

    return HttpResponse(str(configuration.refreshing_client_time))


def change_and_restart_wlan(request):

    return


def home(request):
    return render(request, 'home.html')


def receive_heart_beat(request):
    # it is the test function. return the data of the heart beat
    if request.method != 'POST':
        return HttpResponse('What are doing? No data?')
    try:
        mac_address = request.POST['mac_address']
        ipv6_addresses = request.POST['ipv6_addresses']
        global_ipv6_address = request.POST['global_ipv6_address']
        heart_beat_frequency = request.POST['heart_beat_frequency']
        print(heart_beat_frequency)
    except KeyError:
        return HttpResponseNotAllowed('Wrong format')

    # old faces or new one?
    try:
        client = client_info.objects.get(mac_address=mac_address)
        change_client_info(client,
                           mac_address=mac_address,
                           ipv6_addresses=ipv6_addresses,
                           global_ipv6_address=global_ipv6_address,
                           heart_beat_frequency=heart_beat_frequency)
    except client_info.DoesNotExist:
        create_client_info(mac_address=mac_address,
                           ipv6_addresses=ipv6_addresses,
                           global_ipv6_address=global_ipv6_address,
                           heart_beat_frequency=heart_beat_frequency)
    return HttpResponse('success')
