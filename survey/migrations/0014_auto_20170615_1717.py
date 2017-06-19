# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-15 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0013_auto_20170615_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rc_building',
            name='hvy_ovh',
            field=models.NullBooleanField(default=False, verbose_name='Heavy Overhangs'),
        ),
        migrations.AlterField(
            model_name='rc_building',
            name='pl_irr',
            field=models.NullBooleanField(default=False, verbose_name='Plan Irregularities'),
        ),
        migrations.AlterField(
            model_name='rc_building',
            name='shr_col',
            field=models.NullBooleanField(default=False, verbose_name='Short Column'),
        ),
        migrations.AlterField(
            model_name='rc_building',
            name='vrt_irr',
            field=models.NullBooleanField(default=False, verbose_name='Vertical Irregularities'),
        ),
    ]