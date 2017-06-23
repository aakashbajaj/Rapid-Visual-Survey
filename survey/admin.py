# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import RC_Building, Team, MS_Building, HY_Building
# Register your models here.

admin.site.register(Team)
admin.site.register(HY_Building)

class RCAdminSet(admin.ModelAdmin):
	fieldsets = [
		('ID', {'fields':['uniq', 'bl_id']}),

		('Date and Time', {'fields':['dt_tkn']}),

		('Basic Information', {'fields':['team','addr','no_floor','bas_prsnt','yr_constr', 'yr_aval','yr_extn','acc_level','bl_use','op_bl_use','s_zone',]}),

		('Occupancy', {'fields':['oc_day','oc_night','oc_navl']}),

		('GPS Coordinates', {'fields':['gps_x','gps_y']}),

		('Soft Storey', {'fields':['op_prk','ab_prt','st_shp','tl_htg']}),

		('Vertical Irregularities', {'fields':['pr_stb','bl_slp']}),

		('Plan Irregularities', {'fields':['ir_plc','re_crn']}),

		('Heavy Overhangs', {'fields':['md_hrp','sb_hrp']}),

		('Short Column', {'fields':['shr_col']}),

		('Apparent Quality', {'fields':['ql_mat','maintc']}),

		('Soil Condition', {'fields':['soil_cn']}),

		('Pounding', {'fields':['un_flr','pr_qlt']}),

		('Frame Action', {'fields':['frm_act']}),

		('Building Features', {'fields':['soft_st','vrt_irr','pl_irr','hvy_ovh','ap_qlt','pnding']}),
		
		('Falling Hazards', {'fields':['rf_sign','ac_grl','el_prp','hv_elf','hv_cnp','sb_bal','hv_cld','str_gl']}),

		('Performance Score', {'fields':['perf_score']}),

		('Signature', {'fields':['sign_url']})
	]

	list_display = ('bl_id','dt_tkn')

admin.site.register(RC_Building, RCAdminSet)


class MSAdminSet(admin.ModelAdmin):

	fieldsets = [
		('ID', {'fields':['uniq', 'bl_id']}),

		('Date and Time', {'fields':['dt_tkn']}),

		('Basic Information', {'fields':['team','addr','ty_const','no_floor','bas_prsnt','yr_constr', 'yr_aval','yr_extn','acc_level','bl_use','op_bl_use','s_zone']}),

		('Occupancy', {'fields':['oc_day','oc_night','oc_navl']}),

		('GPS Coordinates', {'fields':['gps_x','gps_y']}),

		('Structural Irregularities', {'fields':['lck_wll', 'hvy_ovh', 're_crn', 'crn_bld']}),

		('Openings', {'fields':['prt_opn', 'irr_opn', 'opn_crn']}),

		('Diaphragm Action', {'fields':['ab_diap', 'lrg_cut']}),

		('Horizontal Bands', {'fields':['plnt_lvl', 'lntl_lvl', 'sill_lvl', 'roof_lvl']}),

		('Arches', {'fields':['arches', 'jck_roof']}),

		('Apparent Quality', {'fields':['ql_mat','maintc']}),

		('Random Rubble Stone Masonary Walls', {'fields':['thk_wll', 'rnd_stn', 'hvy_roof']}),

		('Pounding', {'fields':['cnt_bld', 'pr_qlt']}),

		('Soil Condition', {'fields':['soil_cn']}),

		('Building Features', {'fields':['str_irr', 'diap_ab', 'hrz_bnd', 'arch', 'pnding', 'rub_wll']}),

		('Falling Hazards', {'fields':['rf_sign','ac_grl','el_prp','hv_elf','hv_cnp','sb_bal','hv_cld','str_gl']}),

		('Performance Score', {'fields':['perf_score']}),

		('Signature', {'fields':['sign_url']})	

	]

	list_display = ('bl_id', 'dt_tkn')


admin.site.register(MS_Building, MSAdminSet)