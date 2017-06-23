# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-23 11:07
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0022_auto_20170623_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='hy_building',
            name='oc_navl',
            field=models.BooleanField(default=False, verbose_name='Occupancy Data Not Available?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='hy_building',
            name='yr_aval',
            field=models.BooleanField(default=False, verbose_name='Not Available?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ms_building',
            name='oc_navl',
            field=models.BooleanField(default=False, verbose_name='Occupancy Data Not Available?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ms_building',
            name='ty_const',
            field=models.CharField(choices=[('Brick Masonary', 'Brick Masonary'), ('Composite', 'Composite')], default='Brick Masonary', max_length=50, verbose_name='Type of Construction'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ms_building',
            name='yr_aval',
            field=models.BooleanField(default=False, verbose_name='Not Available?'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hy_building',
            name='no_floor',
            field=models.DecimalField(decimal_places=0, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='No. of Floors'),
        ),
        migrations.AlterField(
            model_name='hy_building',
            name='oc_day',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Day'),
        ),
        migrations.AlterField(
            model_name='hy_building',
            name='oc_night',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Night'),
        ),
        migrations.AlterField(
            model_name='hy_building',
            name='yr_constr',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(1800), django.core.validators.MaxValueValidator(2017)], verbose_name='Year of Construction'),
        ),
        migrations.AlterField(
            model_name='ms_building',
            name='no_floor',
            field=models.DecimalField(decimal_places=0, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='No. of Floors'),
        ),
        migrations.AlterField(
            model_name='ms_building',
            name='oc_day',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Day'),
        ),
        migrations.AlterField(
            model_name='ms_building',
            name='oc_night',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Night'),
        ),
        migrations.AlterField(
            model_name='ms_building',
            name='yr_constr',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(1800), django.core.validators.MaxValueValidator(2017)], verbose_name='Year of Construction'),
        ),
    ]