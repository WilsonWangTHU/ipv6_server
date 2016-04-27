from django.shortcuts import render
from django.http import HttpResponse
# from django.http import HttpResponseNotAllowed
from utils import subClientHeartbeat
from net_data.models import get_CPU_data
from net_data.models import short_term_dataset, configuration, CPU_data
import datetime

default_sample_period = 60
default_sample_volumn = 60
default_heart_beat_period = 600


def home(request):
    return render(request, 'home.html')


def send_heart(request):
    # in this function, the subClient send data to the priClient
    # and return the configuration data, which is the time
    
    return HttpResponse(str())


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
        user_time, kernel_time = get_CPU_data()
        checking_time = str(datetime.datetime.now())
        return HttpResponse(user_time + '\n' + kernel_time + '\n' + checking_time)

    # provide the data
    if path.find('/short_term') != -1:
        database = CPU_data.object.order_by('time')
    else:
        return HttpResponse('You could only ask for /now or /short_term')
    if len(database) == 0:
        return HttpResponse('No data available yet, or the data is corrputed.')

    # TODO: the template!
    data_str = ''
    for i in xrange(len(database)):
        data_str + str(database[i].cpu_unniced_user) + \
            str(database[i].cpu_kernel) + \
            str(database[i].time) + '\n'

    return HttpResponse(data_str)


def record_data(request):
    '''
    record /now /short_term/ will return the current data.
    term data and short term data
    '''
    # TODO: using the regEx to denote the switch, instead of 'find'
    # TODO: HTTPError
    path = request.get_full_path()
    if request.get_host().find('127.0.0.1') == -1:
        return HttpResponse('You are not supposed to be here, mortal.\
                \nReturn while you still can and beg for my mercy')
    if path.find('/short') == -1:
        return HttpResponse('You are not supposed to be here, mortal.\
                \nReturn while you still can and beg for my mercy')

    # processing the dataset
    database = CPU_data.object.all()
    data_config = configuration.object.all()

    # are you first time here? then initialize the configuration
    if len(data_config) != 1:
        configuration.object.all().delete()
        data_config = \
            configuration(short_term_sample_period=default_sample_period,
                          short_term_volumn=default_sample_volumn,
                          heart_beat_sample_period=default_heart_beat_period)
        data_config.save()
    # is the volumn full?
    if len(database) > data_config.short_term_volumn:
        cpu_data = database[0]
        cpu_data.cpu_unniced_user = float(get_CPU_data())
    else:
        cpu_data = CPU_data(cpu_unniced_user=float(get_CPU_data()))
    cpu_data.save()

    return HttpResponse(str(data_config.short_term_sample_period))
