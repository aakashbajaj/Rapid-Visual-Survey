# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-14 20:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0010_auto_20170615_0130'),
    ]

    operations = [
        migrations.CreateModel(
            name='CM_Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniq', models.PositiveIntegerField(blank=True, null=True, verbose_name='Unique ID')),
                ('bl_id', models.CharField(blank=True, max_length=10, null=True, verbose_name='Building ID')),
                ('addr', models.CharField(max_length=200, verbose_name='Address')),
                ('gps_x', models.DecimalField(decimal_places=7, max_digits=10, verbose_name='Latitude')),
                ('gps_y', models.DecimalField(decimal_places=7, max_digits=10, verbose_name='Longtitude')),
                ('oc_day', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Occupancy: Day')),
                ('oc_night', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='Occupancy: Night')),
                ('no_floor', models.DecimalField(decimal_places=0, max_digits=2, verbose_name='No. of Floors')),
                ('bas_prsnt', models.BooleanField(verbose_name='Basement')),
                ('yr_constr', models.DecimalField(decimal_places=0, max_digits=4, verbose_name='Year of Construction')),
                ('yr_extn', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True, verbose_name='Year of Extension(If Any)')),
                ('acc_level', models.CharField(max_length=10, verbose_name='Access Level')),
                ('bl_use', models.CharField(max_length=50, verbose_name='Building Use')),
                ('s_zone', models.PositiveIntegerField(verbose_name='Seismic Zone')),
                ('team', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='survey.Team')),
            ],
            options={
                'verbose_name': 'Composite Building',
                'verbose_name_plural': 'Composite Buildings',
            },
        ),
    ]