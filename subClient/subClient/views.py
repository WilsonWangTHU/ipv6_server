from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed


def home(request):
    return render(request, 'home.html')


def receive_heart_beat(request):
    # it is the test function. return the data of the heart beat
    if request.method != 'POST':
        return HttpResponseNotAllowed('What are doing? No data?')
    data = request.POST['data']
    print(data)
    return HttpResponse(data)
