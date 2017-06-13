# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Team(models.Model):
	mem_1 = models.CharField(max_length = 50, blank = False)
	mem_2 = models.CharField(max_length = 50, blank = True)
	mem_3 = models.CharField(max_length = 50, blank = True)
	mem_4 = models.CharField(max_length = 50, blank = True)

class Building(models.Model):
	team = models.ForeignKey(Team, on_delete = models.DO_NOTHING)
	bl_id = models.PositiveIntegerField()
	addr = models.CharField(max_length = 200)
	gps_x = models.DecimalField(max_digits = 10, decimal_places = 7)
	gps_y = models.DecimalField(max_digits = 10, decimal_places = 7)
	oc_day = models.PositiveIntegerField()
	oc_night = models.PositiveIntegerField()
	no_floor = models.PositiveSmallIntegerField()
	yr_constr = models.PositiveSmallIntegerField()
	yr_extn = models.PositiveSmallIntegerField(blank=True)
	acc_level = models.CharField(max_length = 10)
	bl_use = models.CharField(max_length = 50)
	s_zone = models.PositiveIntegerField()
	
	def __str__(self):
		return self.bl_id

class RC(models.Model):
	
	soft_st = models.BooleanField(default = False)
	vrt_irr = models.BooleanField(default = False)
	pl_irr = models.BooleanField(default = False)
	hvy_ovh = models.BooleanField(default = False)
	shr_col = models.BooleanField(default = False)
	