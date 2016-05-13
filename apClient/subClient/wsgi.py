"""
WSGI config for subClient project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os, sys
import django

apache_conf = os.path.abspath(__file__)
project = os.path.dirname(apache_conf)
workspace = os.path.dirname(project)

sys.path.append(workspace)
sys.path.append('/subClient/subClient')
sys.path.append('/sbin/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

django.setup()

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
