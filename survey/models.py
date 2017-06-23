# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.core.exceptions import ValidationError
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

FEAT_CHOICE = (
	(0, "Absent"),
	(1, "Present")
)

QUAL_CHOICE = (
	(0,"Good"),
	(1,"Moderate"),
	(2,"Poor")
)

SOIL_CHOICE = (
	(0, "Medium"),
	(1, "Hard"),
	(-1, "Soft")
)

FRM_CHOICE = (
	(-1, "Absent"),
	(1, "Present"),
	(0, "Not Sure")
)

IRR_CHOICE = (
	(0,"None"),
	(1,"Moderate"),
	(2,"Extreme")
)

TYP_CHOICE = (
	("Brick Masonary", "Brick Masonary"),
	("Composite", "Composite")
)

OPENING_CHOICE = (
	(0, "Small (<1/3)"),
	(1, "Moderate (1/3 to 2/3)"),
	(2, "Large (>2/3)")
)

BOOL_CHOICE = (
	(1, "Yes"),
	(0, "No")
)

PND_CHOICE = (
	(0, "Absent"),
	(1, "Normal Apparent Condition of Adjacent Building"),
	(2, "Poor Apparent Condition of Adjacent Building")
)


def RC_score(bd):

	# Plan Irregularities	
	if bd.ir_plc is 1 and bd.re_crn is 1:
		bd.pl_irr = 2
	elif (bd.ir_plc is 1 and bd.re_crn is 0) or (bd.ir_plc is 0 and bd.re_crn is 1):
		bd.pl_irr = 1
	else:
		bd.pl_irr = 0

	# Soft Storey
	if bd.op_prk is 1 or bd.ab_prt is 1 or bd.st_shp is 1 or bd.tl_htg is 1:
		bd.soft_st = 1
	else:
		bd.soft_st = 0

	# Vertical Irregularity
	if bd.pr_stb is 1 or bd.bl_slp is 1:
		bd.vrt_irr = 1
	else:
		bd.vrt_irr = 0

	# Heavy Overhangs
	if bd.md_hrp is 1 or bd.sb_hrp is 1:
		bd.hvy_ovh = 1
	else:
		bd.hvy_ovh = 0

	# Apparent Quality
	if bd.ql_mat is 2 and bd.maintc is 2:
		bd.ap_qlt = 2
	elif bd.ql_mat is 0 and bd.maintc is 0:
		bd.ap_qlt = 0
	else:
		bd.ap_qlt = 1

	# Pounding
	if bd.un_flr is 1 or bd.pr_qlt is 1:
		bd.pnding = 1
	else:
		bd.pnding = 0

	buil_flr = int(bd.no_floor)

	if buil_flr is 2:
		flr = 1
	elif buil_flr > 5:
		flr = 6
	else:
		flr = buil_flr

	base_table = {
		 1: {1:150, 2:130, 3:100},
		 3: {1:140, 2:120, 3:90},
		 4: {1:120, 2:100, 3:75},
		 5: {1:100, 2:85, 3:65},
		 6: {1:90, 2:80, 3:60}
	}

	base_score = base_table[flr][bd.s_zone]

	soft_st_f = {1:0, 3:-15, 4:-20, 5:-25, 6:-30}
	hvy_ovh_f = {1:-5, 3:-10, 4:-10, 5:-15, 6:-15}
	ap_qlt_f = {1:-5, 3:-10, 4:-10, 5:-15, 6:-15}
	pnding_f = {1:0, 3:-2, 4:-3, 5:-5, 6:-5}
	bas_prsnt_f = {1:0, 3:3, 4:4, 5:5, 6:5}

	sft = bd.soft_st*soft_st_f[flr]
	vrt = bd.vrt_irr*(-10)
	plir = bd.pl_irr*(-5)
	hvyov = bd.hvy_ovh*hvy_ovh_f[flr]
	apqlty = bd.ap_qlt*ap_qlt_f[flr]
	shrt_clm = bd.shr_col*(-5)
	pound = bd.pnding*2*pnding_f[flr]
	soilcn = bd.soil_cn*10
	frmact = bd.frm_act*10
	bsmt = bd.bas_prsnt*bas_prsnt_f[flr]

	vs = sft + vrt + plir + hvyov + apqlty + shrt_clm + pound + soilcn + frmact + bsmt
	
	perf_sc = base_score + vs

	return perf_sc


def MS_Score(bd):

	# Structural Irregularity
	if bd.lck_wll is 1 or bd.hvy_ovh is 1 or bd.re_crn is 1 or bd.crn_bld is 1:
		bd.str_irr = 1
	else:
		bd.str_irr = 0

	# Apparent Quality
	if bd.ql_mat is 2 and bd.maintc is 2:
		bd.ap_qlt = 2
	elif bd.ql_mat is 0 and bd.maintc is 0:
		bd.ap_qlt = 0
	else:
		bd.ap_qlt = 1

	# Diaphragm Action
	if bd.ab_diap is 1 or bd.lrg_cut is 1:
		bd.diap_ab = 1
	else:
		bd.diap_ab = 0

	# Horizontal Bands
	if bd.plnt_lvl is 1 or bd.lntl_lvl is 1 or bd.sill_lvl is 1 or bd.roof_lvl is 1:
		bd.hrz_bnd = 1
	else:
		bd.hrz_bnd = 0

	# Arches
	if bd.arches is 1 or bd.jck_roof is 1:
		bd.arch = 1
	else:
		bd.arch = 0

	# Pounding
	if bd.cnt_bld is 0:
		bd.pnding = 0
	elif bd.pr_qlt is 1:
		bd.pnding = 2
	else:
		bd.pnding = 1

	# Rubble Wall Masonary
	if bd.thk_wll is 1 or bd.rnd_stn is 1 or bd.hvy_roof is 1:
		bd.rub_wll = 1
	else:
		bd.rub_wll = 0


	buil_flr = int(bd.no_floor)

	if buil_flr is 2:
		flr = 1
	elif buil_flr > 5:
		flr = 5
	else:
		flr = buil_flr

	base_table = {
		 1: {1:150, 2:130, 3:100},
		 3: {1:125, 2:110, 3:85},
		 4: {1:110, 2:90, 3:70},
		 5: {1:70, 2:60, 3:50}
	}

	base_score = base_table[flr][bd.s_zone]

	orn_opn_f = {1:-2, 3:-5, 4:-5, 5:-5}
	pnding_f = {1:0, 3:-3, 4:-5, 5:-5}
	diap_ac_f = {1:-10, 3:-15, 4:-15, 5:-15}
	bas_prsnt_f = {1:0, 3:3, 4:4, 5:5}

	strirr = bd.str_irr * (-10)
	apqlty = bd.ap_qlt * (-10)
	soilcn = bd.soil_cn * (10)
	pound = bd.pnding * pnding_f[flr]
	wlopng = bd.prt_opn * (-5)
	irropn = bd.irr_opn * orn_opn_f[flr]
	diapac = bd.diap_ab * diap_ac_f[flr]
	hrzbnd = bd.hrz_bnd * (20)
	archf = bd.arch * (-10)
	rublwl = bd.rub_wll * (-15)
	bsmnt = bd.bas_prsnt * bas_prsnt_f[flr]

	vs = strirr + apqlty + soilcn + pound + wlopng + irropn + diapac + hrzbnd + archf + rublwl + bsmnt

	perf_sc = base_score + vs

	return perf_sc


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
	oc_day = models.DecimalField("Day", max_digits = 10, decimal_places = 0, validators=[MinValueValidator(0)], blank=True, null=True)
	oc_night = models.DecimalField("Night", max_digits = 10, decimal_places =0, validators=[MinValueValidator(0)], null=True, blank=True)
	oc_navl = models.BooleanField("Not Available?")
	no_floor = models.DecimalField("No. of Floors", max_digits = 2, decimal_places = 0, validators=[MinValueValidator(0)], null=True)
	bas_prsnt = models.PositiveIntegerField("Basement",choices=FEAT_CHOICE)
	yr_constr = models.DecimalField("Year of Construction",null=True, max_digits = 4, decimal_places = 0, validators=[MinValueValidator(1800), MaxValueValidator(timezone.now().year)], blank=True)
	yr_aval = models.BooleanField("Not Available?")
	yr_extn = models.DecimalField("Year of Extension (If Any)",max_digits=4, decimal_places=0, blank=True, null=True, validators=[MinValueValidator(1800), MaxValueValidator(timezone.now().year)])
	bl_use = models.CharField("Building Use",max_length = 50, choices=BLD_USE)
	op_bl_use = models.CharField("If Others, Specify",max_length=50, blank=True, null=True)
	acc_level = models.CharField("Access Level",max_length = 10, choices=ACCESS_CHOICES)
	s_zone = models.PositiveIntegerField("Seismic Zone", choices=SEISMIC_ZONE)
	
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

	def save(self, *args, **kwargs):

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
	gps_x = models.DecimalField("Latitude",max_digits = 9, decimal_places = 7)
	gps_y = models.DecimalField("Longtitude",max_digits = 9, decimal_places = 7)
	oc_day = models.DecimalField("Day", max_digits = 10, decimal_places = 0, validators=[MinValueValidator(0)], blank=True, null=True)
	oc_night = models.DecimalField("Night", max_digits = 10, decimal_places =0, validators=[MinValueValidator(0)], null=True, blank=True)
	oc_navl = models.BooleanField("Not Available?")
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
	ab_diap = models.PositiveIntegerField("Absence of Diaphragms", choices=BOOL_CHOICE)
	lrg_cut = models.PositiveIntegerField("Large Cut-outs in Diaphragm", choices=FEAT_CHOICE)

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


	def save(self, *args, **kwargs):

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
		cleaned_data = super(MS_Building, self).clean()
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
	# Basic Info
	uniq = models.PositiveIntegerField("Unique ID", blank=True, null=True)
	team = models.ForeignKey(Team, on_delete = models.DO_NOTHING)
	bl_id = models.CharField("Building ID",max_length=10, null=True	, blank=True)
	addr = models.CharField("Address",max_length = 200)
	gps_x = models.DecimalField("Latitude",max_digits = 9, decimal_places = 7)
	gps_y = models.DecimalField("Longtitude",max_digits = 9, decimal_places = 7)
	oc_day = models.DecimalField("Day", max_digits = 10, decimal_places = 0, validators=[MinValueValidator(0)], blank=True, null=True)
	oc_night = models.DecimalField("Night", max_digits = 10, decimal_places =0, validators=[MinValueValidator(0)], null=True, blank=True)
	oc_navl = models.BooleanField("Not Available?")
	no_floor = models.DecimalField("No. of Floors", max_digits = 2, decimal_places = 0, validators=[MinValueValidator(0)], null=True)
	bas_prsnt = models.PositiveIntegerField("Basement",choices=FEAT_CHOICE)
	yr_constr = models.DecimalField("Year of Construction",null=True, max_digits = 4, decimal_places = 0, validators=[MinValueValidator(1800), MaxValueValidator(timezone.now().year)], blank=True)
	yr_aval = models.BooleanField("Not Available?")
	yr_extn = models.DecimalField("Year of Extension (If Any)",max_digits=4, decimal_places=0, blank=True, null=True, validators=[MinValueValidator(1800), MaxValueValidator(timezone.now().year)])
	bl_use = models.CharField("Building Use",max_length = 50, choices=BLD_USE)
	op_bl_use = models.CharField("If Others, Specify",max_length=50, blank=True, null=True)
	acc_level = models.CharField("Access Level",max_length = 10, choices=ACCESS_CHOICES)
	s_zone = models.PositiveIntegerField("Seismic Zone", choices=SEISMIC_ZONE)
	
	# Date and Time Taken
	dt_tkn = models.DateTimeField("Taken On", blank=True)

	# Soil Condition
	soil_cn = models.IntegerField("Soil Condtition", choices=SOIL_CHOICE)

	# Signature URL
	sign_url = models.CharField(max_length = 300, validators=[URLValidator])

	# Performance Score
	perf_score = models.IntegerField("Performance Score", blank=True)

	def save(self, *args, **kwargs):

		# Assigning Date and Time
		if self.dt_tkn is None:
			self.dt_tkn = timezone.now()

		tm_cnt = RC_Building.objects.filter(team = self.team).count() + MS_Building.objects.filter(team = self.team).count() + HY_Building.objects.filter(team = self.team).count() + 1

		# Assigning ID to building
		if self.bl_id is None:
			self.bl_id = self.team.name + '-' + str(tm_cnt)

		if self.uniq is None:
			self.uniq = MS_Building.objects.all().count() +  RC_Building.objects.all().count() + HY_Building.objects.all().count() + 1

		return super(HY_Building, self).save(*args, **kwargs)
	
	def __str__(self):
		return self.bl_id

	def clean(self):
		cleaned_data = super(RC_Building, self).clean()
		if self.yr_aval is False and self.yr_constr is None:
			raise ValidationError("Please Enter the Year of Construction")

		if (self.oc_day is None or self.oc_night is None) and self.oc_navl is False:
			raise ValidationError("Please Enter Occupancy Data")

		if str(self.bl_use) == 'Others' and self.op_bl_use is None:
			raise ValidationError("Enter Other Building Use")

	class Meta:
		verbose_name = "Hybrid Building"
		verbose_name_plural = "Hybrid Buildings"