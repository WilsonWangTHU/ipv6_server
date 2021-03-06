from __future__ import unicode_literals

from django.db import models
# Create your models here.


class ipv6_address(models.Model):
    ipv6_address = models.CharField(max_length=100)


class client_info(models.Model):
    mac_address = models.CharField(max_length=20, default='No Mac Address')
    ipv6_addresses = models.ManyToManyField(ipv6_address)
    global_ipv6_address = models.CharField(max_length=100, default="No IPv6 Address")
    ivi_address = models.CharField(max_length=100, default="test_global_address")

    last_active_time = models.DateTimeField(auto_now=True)
    service_start_time = models.DateTimeField(auto_now_add=True)
    heart_beat_frequency = models.IntegerField(default=600)

    # TODO LIST:
    # permission_granted_time = models.DateTimeField()


class wlan_configuration(models.Model):
    channel = models.IntegerField(default=6)
    password = models.CharField(max_length=60, default='1234567890')
    dying_time = models.IntegerField(default=30)  # minutes
    refreshing_client_time = models.IntegerField(default=5)  # minutes


class ivi_address_pool(models.Model):
    # status = 1: usable, = 2: assigned, 3: used
    address = models.CharField(max_length=100)
    pid = models.CharField(max_length=100, default='None')
    mac = models.CharField(max_length=100, default='None')
    status = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now=True)


class prefix_address_pool(models.Model):
    # status = 1: usable, = 2: assigned, 3: used
    address = models.CharField(max_length=100)
    global_address = models.CharField(max_length=100, default='None')
    pid = models.CharField(max_length=100, default='None')
    mac = models.CharField(max_length=100, default='None')
    status = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now=True)
