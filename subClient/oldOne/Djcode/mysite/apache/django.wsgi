# filename:mysite.apache.django.wsgi
# -*- coding:utf-8 -*-
import os, sys
import django

#Calculate the path based on the location of the WSGI script.
apache_configuration= os.path.abspath(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append('/home/wtw/Djcode/mysite/mysite/')
sys.path.append('/usr/sbin/')
sys.path.append('/usr/bin/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
django.setup()

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
