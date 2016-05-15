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
from django.conf import settings
from django.conf.urls.static import static

app_name = 'subClient'

urlpatterns = [
    url(r'^admin/', admin.site.urls),  # the default admin page
    url(r'^home/$', views.home),
    url(r'^/$', views.home),
    url(r'^record/$', views.record_data),
    url(r'^serve/now/$', views.serve_data),
    url(r'^serve/short_term/$', views.serve_data),
    url(r'^sendHeart/$', views.send_heart),
    url(r'^send_prefix_request/$', views.prefix_request),
    url(r'^sendHeart/test/$', views.send_heart),
    url(r'^change_settings/$', views.change_settings),
    # url(r'^heart/$', views.receive_heart_beat),

    url(r'^settings/$', views.show_settings),  # in this page, change the settings
    url(r'^info/$', views.about),
    url(r'^status/$', views.status),
    url(r'^update_route/$', views.update_route),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
