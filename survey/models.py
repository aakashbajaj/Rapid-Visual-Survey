# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.core.exceptions import ValidationError

from rc_score import *
from ms_score import *
from hy_score import *

from choices import *

from gps import *

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
	plot_no = models.CharField("Plot No.", max_length=20, null=True)
	locality = models.CharField("Locality", max_length=200, default="Sector 23")
	city = models.CharField("City", max_length=200, default="Gandhinagar")
	gps_str = models.CharField("Enter Copied Location String", max_length=200, blank=True)
	gps_x = models.DecimalField("Latitude",max_digits = 9, decimal_places = 7, blank=True)
	gps_y = models.DecimalField("Longtitude",max_digits = 9, decimal_places = 7, blank=True)
	oc_day = models.DecimalField("Day", max_digits = 10, decimal_places = 0, validators=[MinValueValidator(0)], blank=True, null=True)
	oc_night = models.DecimalField("Night", max_digits = 10, decimal_places =0, validators=[MinValueValidator(0)], null=True, blank=True)
	oc_navl = models.BooleanField("Occupancy Not Available?")
	no_floor = models.DecimalField("No. of Floors", max_digits = 2, decimal_places = 0, validators=[MinValueValidator(0)], null=True)
	bas_prsnt = models.PositiveIntegerField("Basement",choices=FEAT_CHOICE)
	yr_constr = models.DecimalField("Year of Construction",null=True, max_digits = 4, decimal_places = 0, validators=[MinValueValidator(1800), MaxValueValidator(timezone.now().year)], blank=True)
	yr_aval = models.BooleanField("Not Available?")
	yr_extn = models.DecimalField("Year of Extension (If Any)",max_digits=4, decimal_places=0, blank=True, null=True, validators=[MinValueValidator(1800), MaxValueValidator(timezone.now().year)])
	bl_use = models.CharField("Building Use",max_length = 50, choices=BLD_USE)
	op_bl_use = models.CharField("If Others, Specify",max_length=50, blank=True, null=True)
	acc_level = models.CharField("Access Level",max_length = 10, choices=ACCESS_CHOICES)
	s_zone = models.PositiveIntegerField("Seismic Zone", choices=SEISMIC_ZONE)
	comment = models.CharField("Comments", max_length=500, blank=True, null=True)
	
	# Date and Time Taken
	dt_tkn = models.DateTimeField("Taken On", blank=True)

	# Soil Condition
	soil_cn = models.IntegerField("Soil Condtition", choices=SOIL_CHOICE)

	# Signature URL
	sign_url = models.CharField(max_length = 300, validators=[URLValidator])

	# Performance Score
	perf_score = models.IntegerField("Performance Score", blank=True)

	# Features
	# soft_st = models.PositiveIntegerField("Soft Storey",choices=FEAT_CHOICE, blank=True)
	# vrt_irr = models.PositiveIntegerField("Vertical Irregularities",choices=FEAT_CHOICE)
	# pl_irr = models.PositiveIntegerField("Plan Irregularities",choices=FEAT_CHOICE)
	# hvy_ovh = models.PositiveIntegerField("Heavy Overhangs",choices=FEAT_CHOICE)
	shr_col = models.PositiveIntegerField("Short Column",choices=FEAT_CHOICE)

	# Other Features
	frm_act = models.PositiveIntegerField("Frame Action", choices=FRM_CHOICE)

	soft_st = models.PositiveIntegerField("Soft Storey",choices=FEAT_CHOICE, blank=True)
	# Soft Storey
	op_prk = models.PositiveIntegerField("Open Parking at Ground Level", choices=FEAT_CHOICE)
	ab_prt = models.PositiveIntegerField("Absence of Partition Walls in Ground or Any Intermediate", choices=FEAT_CHOICE)
	st_shp = models.PositiveIntegerField("Storey for Shops or Other Commercial Use", choices=FEAT_CHOICE)
	tl_htg = models.PositiveIntegerField("Taller Height in Ground or Any Other Intermediate Storey", choices=FEAT_CHOICE)

	vrt_irr = models.PositiveIntegerField("Vertical Irregularities",choices=FEAT_CHOICE, blank=True)
	# Vertical Irregularities
	pr_stb = models.PositiveIntegerField("Presence of Setback", choices=FEAT_CHOICE)
	bl_slp = models.PositiveIntegerField("Building on Sloppy Ground", choices=FEAT_CHOICE)

	pl_irr = models.PositiveIntegerField("Plan Irregularities",choices=IRR_CHOICE, blank=True)
	# Plan Irregularities
	ir_plc = models.PositiveIntegerField("Irregular Plan Configuration", choices=FEAT_CHOICE)
	re_crn = models.PositiveIntegerField("Re-Entrant Corners", choices=FEAT_CHOICE)

	hvy_ovh = models.PositiveIntegerField("Heavy Overhangs",choices=FEAT_CHOICE, blank=True)
	# Heavy Overhangs
	md_hrp = models.PositiveIntegerField("Moderate Horizontal Projections", choices=FEAT_CHOICE)
	sb_hrp = models.PositiveIntegerField("Substantial Horizontal Projections", choices=FEAT_CHOICE)

	ap_qlt = models.PositiveIntegerField("Apparent Quality", choices=QUAL_CHOICE, blank=True)
	# Apparent Quality
	ql_mat = models.PositiveIntegerField("Apparent Quality of Construction and Materials", choices=QUAL_CHOICE)
	maintc = models.PositiveIntegerField("Maintainence", choices=QUAL_CHOICE)

	pnding = models.PositiveIntegerField("Pounding", choices=FEAT_CHOICE, blank=True)
	# Pounding
	un_flr = models.PositiveIntegerField("Unaligned Floors", choices=FEAT_CHOICE)
	pr_qlt = models.PositiveIntegerField("Poor Apparent Quality of Adjacent Buildings", choices=FEAT_CHOICE)

	# Falling Hazards
	rf_sign = models.NullBooleanField("Marquees/Hoardings/Roof Signs", default=False)
	ac_grl = models.NullBooleanField("AC Units/Grillwork", default=False)
	el_prp = models.NullBooleanField("Elaborate Parapets", default=False)
	hv_elf = models.NullBooleanField("Heavy Elevation Features", default=False)
	hv_cnp = models.NullBooleanField("Heavy Canopies", default=False)
	sb_bal = models.NullBooleanField("Substantial Balconies", default=False)
	hv_cld = models.NullBooleanField("Heavy Cladding", default=False)
	str_gl = models.NullBooleanField("Structural Glazing", default=False)

	def scratch(self, *args, **kwargs):
		p = self.addr.lower().index('sector')
		self.plot_no = self.addr[:p].strip()

	def save(self, *args, **kwargs):

		# Make Address
		self.addr = self.plot_no + ' ' + self.locality + ' ' + self.city

		# Get GPS Coordinates
		if (self.gps_x is None or self.gps_y is None):
			if self.gps_str is not "":
				getGPScoord(self)

		# Assigning Date and Time
		if self.dt_tkn is None:
			self.dt_tkn = timezone.now()

		tm_cnt = RC_Building.objects.filter(team = self.team).count() + MS_Building.objects.filter(team = self.team).count() + HY_Building.objects.filter(team = self.team).count() + 1
		# Assigning ID to building
		if self.bl_id is None:
			self.bl_id = self.team.name + '-' + str(tm_cnt)

		if self.uniq is None:
			self.uniq = MS_Building.objects.all().count() +  RC_Building.objects.all().count() + HY_Building.objects.all().count() + 1

		self.perf_score = RC_score(self)

		return super(RC_Building, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.bl_id

	def clean(self):
		cleaned_data = super(RC_Building, self).clean()

		if (self.gps_x is None or self.gps_y is None) and self.gps_str is "":
			raise ValidationError("Enter GPS Data Correctly")

		if self.yr_aval is False and self.yr_constr is None:
			raise ValidationError("Please Enter the Year of Construction")

		if (self.oc_day is None or self.oc_night is None) and self.oc_navl is False:
			raise ValidationError("Please Enter Occupancy Data")

		if str(self.bl_use) == 'Others' and self.op_bl_use is None:
			raise ValidationError("Enter Other Building Use")

	class Meta:
		verbose_name = "RC Building"
		verbose_name_plural = "RC Buildings"
	
class MS_Building(models.Model):
	
	# Basic Info
	uniq = models.PositiveIntegerField("Unique ID", blank=True, null=True)
	team = models.ForeignKey(Team, on_delete = models.DO_NOTHING)
	bl_id = models.CharField("Building ID",max_length=10, null=True	, blank=True)
	addr = models.CharField("Address",max_length = 200)
	plot_no = models.CharField("Plot No.", max_length=20, null=True)
	locality = models.CharField("Locality", max_length=200, default="Sector 23")
	city = models.CharField("City", max_length=200, default="Gandhinagar")
	gps_str = models.CharField("Enter Copied Location String", max_length=200, blank=True)
	gps_x = models.DecimalField("Latitude",max_digits = 9, decimal_places = 7, blank=True)
	gps_y = models.DecimalField("Longtitude",max_digits = 9, decimal_places = 7, blank=True)
	oc_day = models.DecimalField("Day", max_digits = 10, decimal_places = 0, validators=[MinValueValidator(0)], blank=True, null=True)
	oc_night = models.DecimalField("Night", max_digits = 10, decimal_places =0, validators=[MinValueValidator(0)], null=True, blank=True)
	oc_navl = models.BooleanField("Occupancy Not Available?")
	no_floor = models.DecimalField("No. of Floors", max_digits = 2, decimal_places = 0, validators=[MinValueValidator(0)], null=True)
	bas_prsnt = models.PositiveIntegerField("Basement",choices=FEAT_CHOICE)
	yr_constr = models.DecimalField("Year of Construction",null=True, max_digits = 4, decimal_places = 0, validators=[MinValueValidator(1800), MaxValueValidator(timezone.now().year)], blank=True)
	yr_aval = models.BooleanField("Not Available?")
	yr_extn = models.DecimalField("Year of Extension (If Any)",max_digits=4, decimal_places=0, blank=True, null=True, validators=[MinValueValidator(1800), MaxValueValidator(timezone.now().year)])
	ty_const = models.CharField("Type of Construction", max_length=50, choices=TYP_CHOICE)
	bl_use = models.CharField("Building Use",max_length = 50, choices=BLD_USE)
	op_bl_use = models.CharField("If Others, Specify",max_length=50, blank=True, null=True)
	acc_level = models.CharField("Access Level",max_length = 10, choices=ACCESS_CHOICES)
	s_zone = models.PositiveIntegerField("Seismic Zone", choices=SEISMIC_ZONE)
	comment = models.CharField("Comments", max_length=500, blank=True, null=True)
	
	# Date and Time Taken
	dt_tkn = models.DateTimeField("Taken On", blank=True)

	# Soil Condition
	soil_cn = models.IntegerField("Soil Condtition", choices=SOIL_CHOICE)

	# Signature URL
	sign_url = models.CharField(max_length = 300, validators=[URLValidator])

	# Performance Score
	perf_score = models.IntegerField("Performance Score", blank=True)

	str_irr = models.PositiveIntegerField("Structural Irregularities", blank=True, choices=FEAT_CHOICE)
	# Structural Irregularities
	lck_wll = models.PositiveIntegerField("Lack of Adequate Walls in both Orthogonal Directions", choices=FEAT_CHOICE)
	hvy_ovh = models.PositiveIntegerField("Heavy Overhangs", choices=FEAT_CHOICE)
	re_crn = models.PositiveIntegerField("Re-entrant Corners", choices=FEAT_CHOICE)
	crn_bld = models.PositiveIntegerField("Corner Building", choices=FEAT_CHOICE)

	prt_opn = models.PositiveIntegerField("Percentage of Openings", choices=OPENING_CHOICE)
	# Openings
	irr_opn = models.PositiveIntegerField("Irregularly Placed Openings", choices=FEAT_CHOICE)
	opn_crn = models.PositiveIntegerField("Openings at Corners of Bearing Wall Interactions", choices=FEAT_CHOICE)

	diap_ab = models.PositiveIntegerField("Diaphragm Action Absent?", choices=BOOL_CHOICE, blank=True)
	# Diaphragm Action
	ab_diap = models.PositiveIntegerField("Absence of Diaphragms", choices=BOOL_CHOICE, default=0)
	lrg_cut = models.PositiveIntegerField("Large Cut-outs in Diaphragm", choices=FEAT_CHOICE, default=0)

	hrz_bnd = models.PositiveIntegerField("Horizontal Bands", choices=FEAT_CHOICE, blank=True)
	# Horizontal Bands
	plnt_lvl = models.PositiveIntegerField("Plinth Level", choices=FEAT_CHOICE)
	lntl_lvl = models.PositiveIntegerField("Lintel Level", choices=FEAT_CHOICE)
	sill_lvl = models.PositiveIntegerField("Sill Level", choices=FEAT_CHOICE)
	roof_lvl = models.PositiveIntegerField("Roof Level", choices=FEAT_CHOICE)

	arch = models.PositiveIntegerField("Arches", choices=FEAT_CHOICE, blank=True)
	# Arches
	arches = models.PositiveIntegerField("Arches", choices=FEAT_CHOICE)
	jck_roof = models.PositiveIntegerField("Jack Arch Roofs", choices=FEAT_CHOICE)

	ap_qlt = models.PositiveIntegerField("Apparent Quality", choices=QUAL_CHOICE, blank=True)
	# Apparent Quality
	ql_mat = models.PositiveIntegerField("Apparent Quality of Construction and Materials", choices=QUAL_CHOICE)
	maintc = models.PositiveIntegerField("Maintainence", choices=QUAL_CHOICE)

	pnding = models.PositiveIntegerField("Pounding", choices=PND_CHOICE, blank=True)
	# Pounding
	cnt_bld = models.PositiveIntegerField("Contiguous Building", choices=FEAT_CHOICE)
	pr_qlt = models.PositiveIntegerField("Poor Apparent Quality of Adjacent Buildings", choices=FEAT_CHOICE)

	soil_cn = models.PositiveIntegerField("Soil Condition", choices=SOIL_CHOICE)

	rub_wll = models.PositiveIntegerField("Random Rubble Stone Masonary", choices=FEAT_CHOICE, blank=True)
	# Random Rubble Stone Masonary
	thk_wll = models.PositiveIntegerField("Thick Walls 600mm or Above", choices=FEAT_CHOICE, default=0)
	rnd_stn = models.PositiveIntegerField("Use of Rounded Stone", choices=FEAT_CHOICE, default=0)
	hvy_roof = models.PositiveIntegerField("Heavy Roofs on URRM Walls", choices=FEAT_CHOICE, default=0)

	# Falling Hazards
	rf_sign = models.NullBooleanField("Marquees/Hoardings/Roof Signs", default=False)
	ac_grl = models.NullBooleanField("AC Units/Grillwork", default=False)
	el_prp = models.NullBooleanField("Elaborate Parapets", default=False)
	hv_elf = models.NullBooleanField("Heavy Elevation Features", default=False)
	hv_cnp = models.NullBooleanField("Heavy Canopies", default=False)
	sb_bal = models.NullBooleanField("Substantial Balconies", default=False)
	hv_cld = models.NullBooleanField("Heavy Cladding", default=False)
	str_gl = models.NullBooleanField("Structural Glazing", default=False)

	def scratch(self, *args, **kwargs):
		p = self.addr.lower().index('sector')
		self.plot_no = self.addr[:p].strip()

	def save(self, *args, **kwargs):

		# Make Address
		self.addr = self.plot_no + ' ' + self.locality + ' ' + self.city

		# Get GPS Coordinates
		if (self.gps_x is None or self.gps_y is None):
			if self.gps_str is not "":
				getGPScoord(self)

		# Assigning Date and Time
		if self.dt_tkn is None:
			self.dt_tkn = timezone.now()

		tm_cnt = RC_Building.objects.filter(team = self.team).count() + MS_Building.objects.filter(team = self.team).count() + HY_Building.objects.filter(team = self.team).count() + 1

		# Assigning ID to building
		if self.bl_id is None:
			self.bl_id = self.team.name + '-' + str(tm_cnt)

		if self.uniq is None:
			self.uniq = MS_Building.objects.all().count() +  RC_Building.objects.all().count() + HY_Building.objects.all().count() + 1

		self.perf_score = MS_Score(self)

		return super(MS_Building, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.bl_id

	def clean(self):
		print self.gps_x is None
		cleaned_data = super(MS_Building, self).clean()

		if (self.gps_x is None or self.gps_y is None) and self.gps_str is "":
			raise ValidationError("Enter GPS Data Correctly")

		if self.yr_aval is False and self.yr_constr is None:
			raise ValidationError("Please Enter the Year of Construction")

		if (self.oc_day is None or self.oc_night is None) and self.oc_navl is False:
			raise ValidationError("Please Enter Occupancy Data")

		if str(self.bl_use) == 'Others' and self.op_bl_use is None:
			raise ValidationError("Enter Other Building Use")

	class Meta:
		verbose_name = "Masonary Building"
		verbose_name_plural = "Masonary Buildings"

class HY_Building(models.Model):
	## Basic Info
	uniq = models.PositiveIntegerField("Unique ID", blank=True, null=True)
	team = models.ForeignKey(Team, on_delete = models.DO_NOTHING)
	bl_id = models.CharField("Building ID",max_length=10, null=True	, blank=True)
	addr = models.CharField("Address",max_length = 200)
	plot_no = models.CharField("Plot No.", max_length=20, null=True)
	locality = models.CharField("Locality", max_length=200, default="Sector 23")
	city = models.CharField("City", max_length=200, default="Gandhinagar")
	gps_str = models.CharField("Enter Copied Location String", max_length=200, blank=True)
	gps_x = models.DecimalField("Latitude",max_digits = 9, decimal_places = 7, blank=True)
	gps_y = models.DecimalField("Longtitude",max_digits = 9, decimal_places = 7, blank=True)
	oc_day = models.DecimalField("Day", max_digits = 10, decimal_places = 0, validators=[MinValueValidator(0)], blank=True, null=True)
	oc_night = models.DecimalField("Night", max_digits = 10, decimal_places =0, validators=[MinValueValidator(0)], null=True, blank=True)
	oc_navl = models.BooleanField("Occupancy Not Available?")
	no_floor = models.DecimalField("No. of Floors", max_digits = 2, decimal_places = 0, validators=[MinValueValidator(0)], null=True)
	bas_prsnt = models.PositiveIntegerField("Basement",choices=FEAT_CHOICE)
	yr_constr = models.DecimalField("Year of Construction",null=True, max_digits = 4, decimal_places = 0, validators=[MinValueValidator(1800), MaxValueValidator(timezone.now().year)], blank=True)
	yr_aval = models.BooleanField("Not Available?")
	yr_extn = models.DecimalField("Year of Extension (If Any)",max_digits=4, decimal_places=0, blank=True, null=True, validators=[MinValueValidator(1800), MaxValueValidator(timezone.now().year)])
	bl_use = models.CharField("Building Use",max_length = 50, choices=BLD_USE)
	op_bl_use = models.CharField("If Others, Specify",max_length=50, blank=True, null=True)
	acc_level = models.CharField("Access Level",max_length = 10, choices=ACCESS_CHOICES)
	s_zone = models.PositiveIntegerField("Seismic Zone", choices=SEISMIC_ZONE)
	comment = models.CharField("Comments", max_length=500, blank=True, null=True)
	
	# Date and Time Taken
	dt_tkn = models.DateTimeField("Taken On", blank=True)

	# Soil Condition
	soil_cn = models.IntegerField("Soil Condtition", choices=SOIL_CHOICE)

	# Signature URL
	sign_url = models.CharField(max_length = 300, validators=[URLValidator])

	# Performance Score
	perf_score = models.IntegerField("Performance Score", blank=True)

	hyb_act = models.IntegerField("Hybrid Action", choices=FRM_CHOICE)

	str_irr = models.PositiveIntegerField("Structural Irregularities", blank=True, choices=FEAT_CHOICE)
	# Structural Irregularities
	lck_wll = models.PositiveIntegerField("Lack of Adequate Walls in both Orthogonal Directions", choices=FEAT_CHOICE)
	hvy_ovh = models.PositiveIntegerField("Heavy Overhangs", choices=FEAT_CHOICE)
	re_crn = models.PositiveIntegerField("Re-entrant Corners", choices=FEAT_CHOICE)
	crn_bld = models.PositiveIntegerField("Corner Building", choices=FEAT_CHOICE)

	prt_opn = models.PositiveIntegerField("Percentage of Openings", choices=OPENING_CHOICE)
	# Openings
	irr_opn = models.PositiveIntegerField("Irregularly Placed Openings", choices=FEAT_CHOICE)
	opn_crn = models.PositiveIntegerField("Openings at Corners of Bearing Wall Interactions", choices=FEAT_CHOICE)

	diap_ab = models.PositiveIntegerField("Diaphragm Action Absent?", choices=BOOL_CHOICE, blank=True)
	# Diaphragm Action
	ab_diap = models.PositiveIntegerField("Absence of Diaphragms", choices=BOOL_CHOICE, default=0)
	lrg_cut = models.PositiveIntegerField("Large Cut-outs in Diaphragm", choices=FEAT_CHOICE, default=0)

	hrz_bnd = models.PositiveIntegerField("Horizontal Bands", choices=FEAT_CHOICE, blank=True)
	# Horizontal Bands
	plnt_lvl = models.PositiveIntegerField("Plinth Level", choices=FEAT_CHOICE)
	lntl_lvl = models.PositiveIntegerField("Lintel Level", choices=FEAT_CHOICE)
	sill_lvl = models.PositiveIntegerField("Sill Level", choices=FEAT_CHOICE)
	roof_lvl = models.PositiveIntegerField("Roof Level", choices=FEAT_CHOICE)

	arch = models.PositiveIntegerField("Arches", choices=FEAT_CHOICE, blank=True)
	# Arches
	arches = models.PositiveIntegerField("Arches", choices=FEAT_CHOICE)
	jck_roof = models.PositiveIntegerField("Jack Arch Roofs", choices=FEAT_CHOICE)

	ap_qlt = models.PositiveIntegerField("Apparent Quality", choices=QUAL_CHOICE, blank=True)
	# Apparent Quality
	ql_mat = models.PositiveIntegerField("Apparent Quality of Construction and Materials", choices=QUAL_CHOICE)
	maintc = models.PositiveIntegerField("Maintainence", choices=QUAL_CHOICE)

	pnding = models.PositiveIntegerField("Pounding", choices=PND_CHOICE, blank=True)
	# Pounding
	cnt_bld = models.PositiveIntegerField("Contiguous Building", choices=FEAT_CHOICE)
	pr_qlt = models.PositiveIntegerField("Poor Apparent Quality of Adjacent Buildings", choices=FEAT_CHOICE)

	soil_cn = models.PositiveIntegerField("Soil Condition", choices=SOIL_CHOICE)

	rub_wll = models.PositiveIntegerField("Random Rubble Stone Masonary", choices=FEAT_CHOICE, blank=True)
	# Random Rubble Stone Masonary
	thk_wll = models.PositiveIntegerField("Thick Walls 600mm or Above", choices=FEAT_CHOICE, default=0)
	rnd_stn = models.PositiveIntegerField("Use of Rounded Stone", choices=FEAT_CHOICE, default=0)
	hvy_roof = models.PositiveIntegerField("Heavy Roofs on URRM Walls", choices=FEAT_CHOICE, default=0)

	# Falling Hazards
	rf_sign = models.NullBooleanField("Marquees/Hoardings/Roof Signs", default=False)
	ac_grl = models.NullBooleanField("AC Units/Grillwork", default=False)
	el_prp = models.NullBooleanField("Elaborate Parapets", default=False)
	hv_elf = models.NullBooleanField("Heavy Elevation Features", default=False)
	hv_cnp = models.NullBooleanField("Heavy Canopies", default=False)
	sb_bal = models.NullBooleanField("Substantial Balconies", default=False)
	hv_cld = models.NullBooleanField("Heavy Cladding", default=False)
	str_gl = models.NullBooleanField("Structural Glazing", default=False)

	def scratch(self, *args, **kwargs):
		p = self.addr.lower().index('sector')
		self.plot_no = self.addr[:p].strip()

	def save(self, *args, **kwargs):

		# Make Address
		self.addr = self.plot_no + ' ' + self.locality + ' ' + self.city

		# Get GPS Coordinates
		if (self.gps_x is None or self.gps_y is None):
			if self.gps_str is not "":
				getGPScoord(self)

		# Assigning Date and Time
		if self.dt_tkn is None:
			self.dt_tkn = timezone.now()

		tm_cnt = RC_Building.objects.filter(team = self.team).count() + MS_Building.objects.filter(team = self.team).count() + HY_Building.objects.filter(team = self.team).count() + 1

		# Assigning ID to building
		if self.bl_id is None:
			self.bl_id = self.team.name + '-' + str(tm_cnt)

		if self.uniq is None:
			self.uniq = MS_Building.objects.all().count() +  RC_Building.objects.all().count() + HY_Building.objects.all().count() + 1

		self.perf_score = HY_Score(self)

		return super(HY_Building, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.bl_id

	def clean(self):

		cleaned_data = super(HY_Building, self).clean()

		if (self.gps_x is None or self.gps_y is None) and self.gps_str is "":
			raise ValidationError("Enter GPS Data Correctly")

		if self.yr_aval is False and self.yr_constr is None:
			raise ValidationError("Please Enter the Year of Construction")

		if (self.oc_day is None or self.oc_night is None) and self.oc_navl is False:
			raise ValidationError("Please Enter Occupancy Data")

		if str(self.bl_use) == 'Others' and self.op_bl_use is None:
			raise ValidationError("Enter Other Building Use")

	class Meta:
		verbose_name = "Composite Building"
		verbose_name_plural = "Composite Buildings"