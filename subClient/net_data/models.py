from __future__ import unicode_literals

from django.db import models
import os
import random

'''
In this file, we define the data models from the subClient.
The subClient need to
1. record the data (both long term and short term)
2. record the settings.
'''


def get_CPU_data():
    result = round(random.random() * 100) / 100.0
    return result


class CPU_data(models.Model):
    cpu_unniced_user = models.FloatField()
    time = models.DateTimeField(auto_now=True)


class short_term_dataset(models.Model):
    data_set = models.ManyToManyField(CPU_data)


class configuration(models.Model):
    short_term_sample_period = models.IntegerField(default=60)
    short_term_volumn = models.IntegerField(default=200)

    heart_beat_sample_period = models.IntegerField(default=600)
