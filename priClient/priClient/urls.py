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
from priClient import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),  # the default admin page
    url(r'^home/$', views.home),  # the home page, display some basic
    url(r'^$', views.home),  # the home page, display some basic
    url(r'^settings/$', views.show_settings),  # in this page, change the settings
    url(r'^change_settings/$', views.change_settings),  # in this page, change the settings
    url(r'^users/(\d+)/$', views.show_users),  # in this page, change the settings
    url(r'^users/$', views.show_users),  # in this page, change the settings
    url(r'^sendHeart/$', views.send_heart),  # in this page, change the settings
    url(r'^iviaddress/$', views.ivi_address),  # in this page, change the settings
    url(r'^change_ivi/$', views.change_ivi),  # in this page, change the settings
    # the auto refresh page for priClient itself
    url(r'^auto_refresh/$', views.refresh_client_info),
    # the heart beat page for subClient
    url(r'^heart/$', views.receive_heart_beat),
    url(r'^prefix/$', views.receive_prefix_request),
    url(r'^info/$', views.about),
]
