# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-19 03:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pythapp', '0005_auto_20170819_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot',
            name='name',
            field=models.CharField(blank=True, default='Sat19Aug17_002242', max_length=80),
        ),
        migrations.AlterField(
            model_name='bot',
            name='style',
            field=models.CharField(default='friendly', max_length=100),
        ),
    ]
