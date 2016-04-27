from __future__ import unicode_literals

from django.db import models
# Create your models here.


class net_data(models.Model):
    record_time = models.DateTimeField(auto_now=True)
    data = models.CharField(max_length=30)

    class Meta:
        ordering = ['record_time']


class client_info(models.Model):
    mac_address = models.CharField(max_length=20)
    ipv6_addresses = models.ForeignKey(str)
    last_time = models.DataTimeField(auto_now=True)
