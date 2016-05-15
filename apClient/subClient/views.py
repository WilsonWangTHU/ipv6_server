from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
import simplejson

from net_data.models import get_CPU_data
from net_data.models import configuration, CPU_data

from utils.subClientHeartbeat import heart_beat_ipv6, request_prefix_ipv6
import datetime
from utils.change_route_table import set_second_ivi_route
import subprocess

default_sample_period = 60
default_sample_volumn = 60
default_heart_beat_period = 600

heart_beat_port_number = 70


def home(request):
    return render(request, 'index.html')


def send_heart(request):
    # in this function, the subClient send data to the priClient
    # and return the configuration data, which is the time
    # from subClientHeartbeat import heart_beat_ipv6

    data_config = configuration.objects.all()

    # are you first time here? then initialize the configuration
    if len(data_config) != 1:
        configuration.objects.all().delete()
        data_config = \
            configuration(short_term_sample_period=default_sample_period,
                          short_term_volumn=default_sample_volumn,
                          heart_beat_sample_period=default_heart_beat_period)
        data_config.save()
    else:
        data_config = data_config[0]

    if request.get_full_path().find('/test') != -1:
        # send the request to localhost 127.0.0.2
        # currently we put the priServer on 127.0.0.2
        result = heart_beat_ipv6(data_config.heart_beat_sample_period,
                                 'wlan0', heart_beat_port_number,
                                 target_host=1, test_mode=2)
    else:
        result = heart_beat_ipv6(data_config.heart_beat_sample_period,
                                 'wlan0', heart_beat_port_number,
                                 target_host=0, test_mode=0)  # using the intranet

    if result.find('success') == -1:  # retry immediately
        return HttpResponse('failure\n' + str(data_config.heart_beat_sample_period))

    return HttpResponse(result + '\n' + str(data_config.heart_beat_sample_period))


def serve_data(request):
    '''
    /serve/now/ or serve/st/ will return the current data
    and short term data
    '''

    # TODO: using the regEx to denote the switch, instead of 'find'
    # TODO: HTTPError
    path = request.get_full_path()

    # provide the real time data
    if path.find('/now') != -1:
        user_time = get_CPU_data()
        checking_time = str(datetime.datetime.now())
        return HttpResponse(user_time + '\n' + '\n' + checking_time)

    # provide the data
    if path.find('/short_term') != -1:
        database = CPU_data.objects.order_by('time')
    else:
        return HttpResponse('You could only ask for /now or /short_term')
    if len(database) == 0:
        return HttpResponse('No data available yet, or the data is corrputed.')

    # TODO: the template!
    data_str = ''
    for i in xrange(len(database)):
        data_str = data_str + str(database[i].cpu_unniced_user) + \
            ' ' + str(database[i].time) + '\n'

    return HttpResponse(data_str)


def record_data(request):
    '''
    /record/now /short_term/ will return the current data.
    '''
    # TODO: using the regEx to denote the switch, instead of 'find'
    # TODO: HTTPError
    # path = request.get_full_path()
    if request.get_host().find('127.0.0.1') == -1:
        return HttpResponse('You are not supposed to be here, mortal.\
                \nReturn while you still can and beg for my mercy')
    # processing the dataset
    database = CPU_data.objects.order_by('time')
    data_config = configuration.objects.all()

    # are you first time here? then initialize the configuration
    if len(data_config) != 1:
        configuration.objects.all().delete()
        data_config = \
            configuration(short_term_sample_period=default_sample_period,
                          short_term_volumn=default_sample_volumn,
                          heart_beat_sample_period=default_heart_beat_period)
        data_config.save()
    else:
        data_config = data_config[0]

    # is the volumn full?
    if len(database) >= data_config.short_term_volumn:
        for i in xrange(len(database) - data_config.short_term_volumn + 1):
            database[i].delete()

    value = -1
    value = get_CPU_data()
    value = float(get_CPU_data())
    print(value)
    cpu_data = CPU_data(cpu_unniced_user=value)
    cpu_data.save()

    return HttpResponse(str(data_config.short_term_sample_period))


def show_settings(request):
    # ssl needed or admin needed
    data_config = configuration.objects.all()

    # are you first time here? then initialize the configuration
    if len(data_config) != 1:
        configuration.objects.all().delete()
        data_config = configuration()
    else:
        data_config = data_config[0]

    return render(request, 'show_settings.html',
                  {'settings': data_config})

    if request.method != 'POST':
        return HttpResponseNotAllowed('Get out')

    sample_period = request.POST['sample_period']
    sample_volumn = request.POST['sample_volumn']
    heart_beat_period = request.POST['heart_beat_period']

    data_config = configuration.objects.all()

    # are you first time here? then initialize the configuration
    if len(data_config) != 1:
        configuration.objects.all().delete()
        data_config = \
            configuration(short_term_sample_period=sample_period,
                          short_term_volumn=sample_volumn,
                          heart_beat_sample_period=heart_beat_period)
    else:
        data_config = data_config[0]
        data_config.short_term_sample_period = sample_period
        data_config.short_term_volumn = sample_volumn
        data_config.heart_beat_sample_period = heart_beat_period

    data_config.save()

    return HttpResponse('Nice Try!')


def change_settings(request):
    # TODO: ssl needed or admin needed
    data_config = configuration.objects.all()

    # are you first time here? then initialize the configuration
    if len(data_config) != 1:
        configuration.objects.all().delete()
        data_config = configuration()
    else:
        data_config = data_config[0]

    if request.method != 'POST':
        return render(request, 'show_settings.html',
                      {'settings': data_config})
    # the change
    if 'short_term_sample_period' in request.POST:
        if request.POST['short_term_sample_period'].isdigit() and request.POST['short_term_sample_period'] != '':
            data_config.short_term_sample_period = request.POST['short_term_sample_period']
    if 'short_term_volumn' in request.POST:
        if request.POST['short_term_volumn'].isdigit() and request.POST['short_term_volumn'] != '':
            data_config.short_term_volumn = request.POST['short_term_volumn']
    if 'heart_beat_sample_period' in request.POST:
        if request.POST['heart_beat_sample_period'].isdigit() and request.POST['heart_beat_sample_period'] != '':
            data_config.heart_beat_sample_period = request.POST['heart_beat_sample_period']

    data_config.save()

    return render(request, 'show_settings.html',
                  {'settings': data_config, 'Congrats': 'Successfully Changed The Settings'})


def about(request):
    return render(request, 'info.html')


def status(request):
    # first generate the json data
    cpu_data_client = CPU_data.objects.order_by('time')
    time_data = []
    cpu_data = []
    for single_data in cpu_data_client:
        delta_time = single_data.time.replace(tzinfo=None) \
            - cpu_data_client[0].time.replace(tzinfo=None)
        time_data.append(delta_time.total_seconds())
        cpu_data.append(single_data.cpu_unniced_user)

    data = {'time_data': time_data}
    data['cpu_data'] = cpu_data
    data['xrange'] = max(data['time_data'])
    data['yrange'] = max(data['cpu_data'])
    js_data = simplejson.dumps(data)
    return render(request, 'status.html', {'js_data': js_data, 'start_time': cpu_data_client[0].time, 'end_time': cpu_data_client[len(cpu_data_client) - 1].time, 'num': len(cpu_data_client)})


def prefix_request(request):
    # in this function, the subClient send data to the priClient
    # and return the configuration data, which is the time
    # from subClientHeartbeat import heart_beat_ipv6

    data_config = configuration.objects.all()

    # are you first time here? then initialize the configuration
    if len(data_config) != 1:
        configuration.objects.all().delete()
        data_config = \
            configuration(short_term_sample_period=default_sample_period,
                          short_term_volumn=default_sample_volumn,
                          heart_beat_sample_period=default_heart_beat_period)
        data_config.save()
    else:
        data_config = data_config[0]

    if request.get_full_path().find('/test') != -1:
        # send the request to localhost 127.0.0.2
        # currently we put the priServer on 127.0.0.2
        result = request_prefix_ipv6(data_config.heart_beat_sample_period,
                                     'wlan0', heart_beat_port_number,
                                     target_host=1, test_mode=2)
    else:
        result = request_prefix_ipv6(data_config.heart_beat_sample_period,
                                     'wlan0', heart_beat_port_number,
                                     target_host=0, test_mode=0)  # using the intranet

    if result.find('success') == -1:  # retry immediately
        return HttpResponse('failure\n' + str(data_config.heart_beat_sample_period))

    return HttpResponse(result + '\n' + str(data_config.heart_beat_sample_period))


def update_route(request):
    if request.method != 'POST':
        return HttpResponse('What are doing? No data?')
    try:
        target_address = request.POST['target_address']
        target_via = request.POST['target_via']
    except KeyError:
        return HttpResponseNotAllowed('Wrong format')
    subprocess.Popen('sudo ip -6 route add ' + target_address + ' dev wlan1', shell=True)
    return HttpResponse('success')

    result = set_second_ivi_route(target_address, target_via, 'wlan1')

    return HttpResponse('success')
