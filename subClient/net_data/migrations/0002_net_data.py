# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-26 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('net_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='net_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_time', models.DateField(auto_now=True)),
                ('record_date', models.TimeField(auto_now=True)),
                ('data', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['record_time'],
            },
        ),
    ]
