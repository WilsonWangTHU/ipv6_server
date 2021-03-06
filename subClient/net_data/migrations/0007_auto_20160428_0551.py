# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 05:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('net_data', '0006_auto_20160427_0806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='long_term_dataset',
            name='data_set',
        ),
        migrations.RemoveField(
            model_name='configuration',
            name='long_term_sample_period',
        ),
        migrations.RemoveField(
            model_name='configuration',
            name='long_term_volumn',
        ),
        migrations.RemoveField(
            model_name='cpu_data',
            name='cpu_kernel',
        ),
        migrations.AddField(
            model_name='configuration',
            name='heart_beat_sample_period',
            field=models.IntegerField(default=600),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='short_term_sample_period',
            field=models.IntegerField(default=60),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='short_term_volumn',
            field=models.IntegerField(default=200),
        ),
        migrations.DeleteModel(
            name='long_term_dataset',
        ),
    ]
