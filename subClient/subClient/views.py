from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed

from net_data.models import get_CPU_data
from net_data.models import configuration, CPU_data

from utils.subClientHeartbeat import heart_beat_ipv6
import datetime

default_sample_period = 60
default_sample_volumn = 60
default_heart_beat_period = 600

heart_beat_port_number = 8000


def home(request):
    return render(request, 'home.html')


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
                                 target_host=1, test_mode=0)
    if result is False:  # retry immediately
        return HttpResponse('0')
    return HttpResponse(str(data_config.heart_beat_sample_period))


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

    cpu_data = CPU_data(cpu_unniced_user=float(get_CPU_data()))
    cpu_data.save()

    return HttpResponse(str(data_config.short_term_sample_period))


def settings(request):
    # ssl needed or admin needed
    if request.method != 'POST':
        return HttpResponseNotAllowed('Get out')

    sample_period = request.POST['sample_period']
    sample_volumn = request.POST['sample_volumn']
    heart_beat_period = request.POST['heart_beat_period']

    data_config = configuration.objects.all()

    # are you first time here? then initialize the configuration
    print(len(data_config))
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
