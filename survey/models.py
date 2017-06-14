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

	def __str__(self):
		return self.name

class RC_Building(models.Model):
	# Basic Info
	uniq = models.PositiveIntegerField("Unique ID", blank=True, null=True)
	team = models.ForeignKey(Team, on_delete = models.DO_NOTHING, blank=True)
	bl_id = models.CharField("Building ID",max_length=10, primary_key = True, blank=True)
	addr = models.CharField("Address",max_length = 200)
	gps_x = models.DecimalField("Latitude",max_digits = 10, decimal_places = 7)
	gps_y = models.DecimalField("Longtitude",max_digits = 10, decimal_places = 7)
	oc_day = models.DecimalField("Occupancy: Day", max_digits = 10, decimal_places = 0)
	oc_night = models.DecimalField("Occupancy: Night", max_digits = 10, decimal_places =0)
	no_floor = models.DecimalField("No. of Floors", max_digits = 2, decimal_places = 0)
	bas_prsnt = models.BooleanField("Basement", blank = True, )
	yr_constr = models.DecimalField("Year of Construction", max_digits = 4, decimal_places = 0)
	yr_extn = models.DecimalField("Year of Extension(If Any)",max_digits=4, decimal_places=0, blank=True, null=True)
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
		print(self.yr_constr)
		print(self.yr_extn)
		print('\n')
		print(self.yr_extn is None)
		tm_cnt = RC_Building.objects.filter(team = self.team).count() + 1
		print(tm_cnt)
		self.bl_id = self.team.name + '-' + str(tm_cnt)
		print(self.bl_id)
		self.uniq = RC_Building.objects.all().count() + 1
		super(RC_Building, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.bl_id

	class Meta:
		verbose_name = "RC Building"
		verbose_name_plural = "RC Buildings"
	
class MS_Building(models.Model):
	# Basic Info
	uniq = models.PositiveIntegerField("Unique ID", unique=True)
	team = models.ForeignKey(Team, on_delete = models.DO_NOTHING, blank=True)
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
		tm_cnt = Building.objects.filter(team = self.team).count() + 1
		bl_id = self.team.name + '-' + str(tm_cnt)
		uniq = Building.objects.all().count() + 1
		super(RC_Building, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.bl_id

	class Meta:
		verbose_name = "Masonary Building"
		verbose_name_plural = "Masonary Buildings"

class HY_Building(models.Model):
	# Basic Info
	uniq = models.PositiveIntegerField("Unique ID", unique=True)
	team = models.ForeignKey(Team, on_delete = models.DO_NOTHING, blank=True)
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
		tm_cnt = Building.objects.filter(team = self.team).count() + 1
		bl_id = self.team.name + '-' + str(tm_cnt)
		uniq = Building.objects.all().count() + 1
		super(RC_Building, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.bl_id

	class Meta:
		verbose_name = "Hybrid Building"
		verbose_name_plural = "Hybrid Buildings"