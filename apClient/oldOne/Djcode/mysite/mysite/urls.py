from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
from mysite import views, views_new
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello world")

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),

    #url(r'mac_error/$', views.mac_error),

    #url(r'guide_page/0/$',views.guide_zero),
    #url(r'guide_page/0.5/$',views.guide_half),
    #url(r'guide_page/1/1/$',views.guide_one_one),
    #url(r'guide_page/1/2/$',views.guide_one_two),
    #url(r'guide_page/2/1/$',views.guide_two_one),
    #url(r'guide_page/2/2/$',views.guide_two_two),
    
    #url(r'first_config/$',views.first_config),

    #url(r'userauth/$',views.userauth),
    #url(r'userauth/result/$',views.guide_two_two),
    #url(r'changename/$',views.changename),
    #url(r'changename/result/$',views.cnsubmit),
    
    #url(r'logout1/$',views.logout1),
    
    #url(r'logout2/$',views.logout2),
    

    #url(r'^$',views.test),
    #url(r'^$',views.info),
    #url(r'tunnel type/choose/$',views.choose_tunnel),
    #url(r'tunnel type/delete/$',views.delete_tunnel),
    #url(r'logout/$',views.logout ),
    #url(r'^static/(?P<path>.*)', 'django.views.static.serve', {'document_root': '/home/wtw/Djcode/mysite/static/'}),
    url(r'^$',views_new.info),
    #url(r'tunnel check/$',views_new.ifconfig),
    #url(r'error/$',views_new.error),
    url(r'^hello/$', hello),
)
