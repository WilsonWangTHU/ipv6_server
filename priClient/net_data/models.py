from __future__ import unicode_literals

from django.db import models
# Create your models here.


class ipv6_address(models.Model):
    ipv6_address = models.CharField(max_length=30)


class client_info(models.Model):
    mac_address = models.CharField(max_length=20, default='test_test_test')
    ipv6_addresses = models.ManyToManyField(ipv6_address)
    global_ipv6_address = models.CharField(max_length=20, default="test_global_address")

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
