# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Team(models.Model):
	name = models.CharField(max_length = 2, unique = True)
	mem_1 = models.CharField("Member 1",max_length = 50, blank = False)
	mem_2 = models.CharField("Member 2",max_length = 50, blank = True)
	mem_3 = models.CharField("Member 3",max_length = 50, blank = True)
	mem_4 = models.CharField("Member 4",max_length = 50, blank = True)

class RC_Building(models.Model):
	# Basic Info
	uniq = models.PositiveIntegerField("Unique ID", unique=True)
	team = models.ForeignKey("Team", Team, on_delete = models.DO_NOTHING, blank=True)
	bl_id = models.CharField("Building ID",max_length=10, primary_key = True)
	addr = models.CharField("Address",max_length = 200)
	gps_x = models.DecimalField("Latitude",max_digits = 10, decimal_places = 7)
	gps_y = models.DecimalField("Longtitude",max_digits = 10, decimal_places = 7)
	oc_day = models.PositiveIntegerField("Occupancy: Day")
	oc_night = models.PositiveIntegerField("Occupancy: Night")
	no_floor = models.PositiveSmallIntegerField("No. of Floors")
	yr_constr = models.PositiveSmallIntegerField("Year of Construction")
	yr_extn = models.PositiveSmallIntegerField("Year of Extension(If Any)",blank=True)
	acc_level = models.CharField("Access Level",max_length = 10)
	bl_use = models.CharField("Building Use",max_length = 50)
	s_zone = models.PositiveIntegerField("Seismic Zone")
	
	# Features
	soft_st = models.BooleanField("Soft Storey",default = False)
	vrt_irr = models.BooleanField("Vertical Irregularities",default = False)
	pl_irr = models.BooleanField(default = False)
	hvy_ovh = models.BooleanField(default = False)
	shr_col = models.BooleanField(default = False)

	def save(self, *args, **kwargs):
		tm_cnt = Building.objects.filter(team = self.team).count() + 1
		bl_id = self.team.name + '-' + str(tm_cnt)
		uniq = Building.objects.all().count() + 1
		super(RC_Building, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.bl_id
	
class MS_Building(models.Model):
	# Basic Info
	uniq = models.PositiveIntegerField("Unique ID", unique=True)
	team = models.ForeignKey("Team",Team, on_delete = models.DO_NOTHING)
	bl_id = models.CharField("Building ID",max_length=10, primary_key = True)
	addr = models.CharField("Address",max_length = 200)
	gps_x = models.DecimalField("Latitude",max_digits = 10, decimal_places = 7)
	gps_y = models.DecimalField("Longtitude",max_digits = 10, decimal_places = 7)
	oc_day = models.PositiveIntegerField("Occupancy: Day")
	oc_night = models.PositiveIntegerField("Occupancy: Night")
	no_floor = models.PositiveSmallIntegerField("No. of Floors")
	yr_constr = models.PositiveSmallIntegerField("Year of Construction")
	yr_extn = models.PositiveSmallIntegerField("Year of Extension(If Any)",blank=True)
	acc_level = models.CharField("Access Level",max_length = 10)
	bl_use = models.CharField("Building Use",max_length = 50)
	s_zone = models.PositiveIntegerField("Seismic Zone")
	
	def save(self, *args, **kwargs):
		super(RC_Building, self).save(*args, **kwargs)
	

class HY_Building(models.Model):
	# Basic Info
	uniq = models.PositiveIntegerField("Unique ID", unique=True)
	team = models.ForeignKey("Team",Team, on_delete = models.DO_NOTHING)
	bl_id = models.CharField("Building ID",max_length=5, primary_key = True)
	addr = models.CharField("Address",max_length = 200)
	gps_x = models.DecimalField("Latitude",max_digits = 10, decimal_places = 7)
	gps_y = models.DecimalField("Longtitude",max_digits = 10, decimal_places = 7)
	oc_day = models.PositiveIntegerField("Occupancy: Day")
	oc_night = models.PositiveIntegerField("Occupancy: Night")
	no_floor = models.PositiveSmallIntegerField("No. of Floors")
	yr_constr = models.PositiveSmallIntegerField("Year of Construction")
	yr_extn = models.PositiveSmallIntegerField("Year of Extension(If Any)",blank=True)
	acc_level = models.CharField("Access Level",max_length = 10)
	bl_use = models.CharField("Building Use",max_length = 50)
	s_zone = models.PositiveIntegerField("Seismic Zone")
	
	def save(self, *args, **kwargs):
		super(RC_Building, self).save(*args, **kwargs)
	