from __future__ import unicode_literals

from django.db import models
# Create your models here.


class net_data(models.Model):
    record_time = models.DateTimeField(auto_now=True)
    data = models.CharField(max_length=30)

    class Meta:
        ordering = ['record_time']


class ipv6_address(models.Model):
    ipv6_address = models.CharField(max_length=30)


class client_info(models.Model):
    mac_address = models.CharField(max_length=20)
    ipv6_addresses = models.ManyToManyField(ipv6_address)
    global_ipv6_address = models.CharField(max_length=20)

    last_active_time = models.DateTimeField(auto_now=True)
    service_start_time = models.DateTimeField()

    # TODO LIST:
    # permission_granted_time = models.DateTimeField()
    # heart_beat_frequency = models.FloatField()
