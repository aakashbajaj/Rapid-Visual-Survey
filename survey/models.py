# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# Create your models here.

# Choices for all fields
ACCESS_CHOICES = (
	('FULL', 'FULL'),
	('PARTIAL', 'PARTIAL'),
	('NO', 'NO')
)

SEISMIC_ZONE = (
	( 1, 'II and III'),
	( 2, 'IV'),
	( 3, 'V')
)

BLD_USE = (
	('Residential','Residential'),
	('Commercial','Commercial'),
	('Mixed','Mixed'),
	('Others','Others')
)

BASM_CHOICE = (
	('P', "Presesnt"),
	('A', "Absent")
)

FEAT_CHOICE = (
	(0, "Absent"),
	(1, "Present")
)

QUAL_CHOICE = (
	(0,"Good"),
	(1,"Moderate"),
	(2,"Poor")
)



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
	team = models.ForeignKey(Team, on_delete = models.DO_NOTHING)
	bl_id = models.CharField("Building ID",max_length=10, null=True	, blank=True)
	addr = models.CharField("Address",max_length = 200)
	gps_x = models.DecimalField("Latitude",max_digits = 9, decimal_places = 7)
	gps_y = models.DecimalField("Longtitude",max_digits = 9, decimal_places = 7)
	oc_day = models.DecimalField("Day", max_digits = 10, decimal_places = 0)
	oc_night = models.DecimalField("Night", max_digits = 10, decimal_places =0)
	no_floor = models.DecimalField("No. of Floors", max_digits = 2, decimal_places = 0)
	bas_prsnt = models.CharField("Basement",max_length=1, choices=BASM_CHOICE)
	yr_constr = models.DecimalField("Year of Construction", max_digits = 4, decimal_places = 0)
	yr_extn = models.DecimalField("Year of Extension (If Any)",max_digits=4, decimal_places=0, blank=True, null=True)
	bl_use = models.CharField("Building Use",max_length = 50, choices=BLD_USE)
	op_bl_use = models.CharField("If Others, Specify",max_length=50, blank=True, null=True)
	acc_level = models.CharField("Access Level",max_length = 10, choices=ACCESS_CHOICES)
	s_zone = models.PositiveIntegerField("Seismic Zone", choices=SEISMIC_ZONE)
	
	# Date and Time Taken
	dt_tkn = models.DateTimeField("Taken On", blank=True)

	# Features
	# soft_st = models.PositiveIntegerField("Soft Storey",choices=FEAT_CHOICE, blank=True)
	# vrt_irr = models.PositiveIntegerField("Vertical Irregularities",choices=FEAT_CHOICE)
	# pl_irr = models.PositiveIntegerField("Plan Irregularities",choices=FEAT_CHOICE)
	# hvy_ovh = models.PositiveIntegerField("Heavy Overhangs",choices=FEAT_CHOICE)
	shr_col = models.PositiveIntegerField("Short Column",choices=FEAT_CHOICE)

	# Other Features
	frm_act = models.NullBooleanField("Frame Action Present")


	soft_st = models.PositiveIntegerField("Soft Storey",choices=FEAT_CHOICE, blank=True, default=0)
	# Soft Storey
	op_prk = models.PositiveIntegerField("Open Parking at Ground Level", choices=FEAT_CHOICE)
	ab_prt = models.PositiveIntegerField("Absence of Partition Walls in Ground or Any Intermediate", choices=FEAT_CHOICE)
	st_shp = models.PositiveIntegerField("Storey for Shops or Other Commercial Use", choices=FEAT_CHOICE)
	tl_htg = models.PositiveIntegerField("Taller Height in Ground or Any Other Intermediate Storey", choices=FEAT_CHOICE)


	vrt_irr = models.PositiveIntegerField("Vertical Irregularities",choices=FEAT_CHOICE, blank=True, default=0)
	# Vertical Irregularities
	pr_stb = models.PositiveIntegerField("Presence of Setback", choices=FEAT_CHOICE)
	bl_slp = models.PositiveIntegerField("Building on Sloppy Ground", choices=FEAT_CHOICE)


	pl_irr = models.PositiveIntegerField("Plan Irregularities",choices=FEAT_CHOICE, blank=True, default=0)
	# Plan Irregularities
	ir_plc = models.PositiveIntegerField("Irregular Plan Configuration", choices=FEAT_CHOICE)
	re_crn = models.PositiveIntegerField("Re-Entrant Corners", choices=FEAT_CHOICE)


	hvy_ovh = models.PositiveIntegerField("Heavy Overhangs",choices=FEAT_CHOICE, blank=True, default=0)
	# Heavy Overhangs
	md_hrp = models.PositiveIntegerField("Moderate Horizontal Projections", choices=FEAT_CHOICE)
	sb_hrp = models.PositiveIntegerField("Substantial Horizontal Projections", choices=FEAT_CHOICE)


	ap_qlt = models.PositiveIntegerField("Apparent Quality", choices=QUAL_CHOICE, blank=True, default=0)
	# Apparent Quality
	ql_mat = models.PositiveIntegerField("Apparent Quality of Construction and Materials", choices=QUAL_CHOICE)
	maintc = models.PositiveIntegerField("Maintainence", choices=QUAL_CHOICE)


	# Falling Hazards
	rf_sign = models.NullBooleanField("Marquees/Hoardings/Roof Signs", default=False)
	ac_grl = models.NullBooleanField("AC Units/Grillwork", default=False)
	el_prp = models.NullBooleanField("Elaborate Parapets", default=False)
	hv_elf = models.NullBooleanField("Heavy Elevation Features", default=False)
	hv_cnp = models.NullBooleanField("Heavy Canopies", default=False)
	sb_bal = models.NullBooleanField("Substantial Balconies", default=False)
	hv_cld = models.NullBooleanField("Heavy Cladding", default=False)
	str_gl = models.NullBooleanField("Structural Glazing", default=False)

	# Signature URL
	sign_url = models.CharField(max_length = 300)

	def save(self, *args, **kwargs):
		self.soft_st = True
		print(self.yr_constr)
		print(self.yr_extn)
		print('\n')
		print(self.yr_extn is None)
		print('\n')
		print(self.bl_id is None)
		print(self.uniq is None)
		tm_cnt = RC_Building.objects.filter(team = self.team).count() + 1
		print(tm_cnt)


		# Assigning Date and Time
		if self.dt_tkn is None:
			self.dt_tkn = timezone.now()

		# Assigning ID to building
		if self.bl_id is None:
			self.bl_id = self.team.name + '-' + str(tm_cnt)
		print(self.bl_id)
		if self.uniq is None:
			self.uniq = RC_Building.objects.all().count() + 1
		
		return super(RC_Building, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.bl_id

	class Meta:
		verbose_name = "RC Building"
		verbose_name_plural = "RC Buildings"
	
class MS_Building(models.Model):
	# Basic Info
	uniq = models.PositiveIntegerField("Unique ID", blank=True, null=True)
	team = models.ForeignKey(Team, on_delete = models.DO_NOTHING)
	bl_id = models.CharField("Building ID",max_length=10, null=True	, blank=True)
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
	uniq = models.PositiveIntegerField("Unique ID", blank=True, null=True)
	team = models.ForeignKey(Team, on_delete = models.DO_NOTHING)
	bl_id = models.CharField("Building ID",max_length=10, null=True	, blank=True)
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