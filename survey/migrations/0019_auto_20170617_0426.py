# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 22:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0018_auto_20170617_0425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rc_building',
            name='s_zone',
            field=models.PositiveIntegerField(choices=[(1, 'II and III'), (2, 'IV'), (3, 'V')], verbose_name='Seismic Zone'),
        ),
    ]