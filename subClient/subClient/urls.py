"""subClient URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from subClient import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),  # the default admin page
    url(r'^home/$', views.home),
    url(r'^record/$', views.record_data),
    url(r'^serve/now/$', views.serve_data),
    url(r'^serve/short_term/$', views.serve_data),
    url(r'^sendHeart/$', views.send_heart),
    url(r'^settings/$', views.settings),
    # url(r'^heart/$', views.receive_heart_beat),
]
