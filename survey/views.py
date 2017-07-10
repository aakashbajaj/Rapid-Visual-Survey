# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from models import *

import csv
import xlsxwriter, StringIO
from time import strftime, gmtime, localtime

def index(request):
	return HttpResponse("Hello");

@staff_member_required
def BuildingExcel(request, **kwargs):
	rcbuilding = RC_Building.objects.all().order_by('uniq')
	msbuilding = MS_Building.objects.all().order_by('uniq')
	hybuilding = HY_Building.objects.all().order_by('uniq')
	output = StringIO.StringIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet('Sheet1')
	date_format = workbook.add_format({'num_format':'mmmm dd yyyy'})
	worksheet.write(0, 0, "Generated:")
	generated = strftime("%d-%m-%Y %H:%M:%S IST", localtime())
	worksheet.write(0,1, generated)
	bold = workbook.add_format({'bold': True})

	worksheet.write(1,0, "Unique ID", bold)
	worksheet.write(1,1, "Building ID", bold)
	worksheet.write(1,2, "Address", bold)
	worksheet.write(1,3, "Type", bold)
	worksheet.write(1,4, "No. of Floors", bold)
	worksheet.write(1,5, "GPS X", bold)
	worksheet.write(1,6, "GPS Y", bold)
	worksheet.write(1,7, "Day Occupancy", bold)
	worksheet.write(1,8, "Night Occupancy", bold)
	worksheet.write(1,9, "RVS Score", bold)
	worksheet.write(1,10, "Basement", bold)
	worksheet.write(1,11, "Heavy Overhangs", bold)
	worksheet.write(1,12, "Pounding", bold)
	worksheet.write(1,13, "Year of Construction", bold)

	for i, p in enumerate(rcbuilding):
		worksheet.write(i+2,0, p.uniq)
		worksheet.write(i+2,1, p.bl_id)
		worksheet.write(i+2,2, p.addr)
		worksheet.write(i+2,3, "RC")
		worksheet.write(i+2,4, p.no_floor)
		worksheet.write(i+2,5, p.gps_x)
		worksheet.write(i+2,6, p.gps_y)
		worksheet.write(i+2,7, p.oc_day)
		worksheet.write(i+2,8, p.oc_night)
		worksheet.write(i+2,9, p.perf_score)
		worksheet.write(i+2,10, p.bas_prsnt)
		worksheet.write(i+2,11, p.hvy_ovh)
		worksheet.write(i+2,12, p.pnding)
		worksheet.write(i+2,13, p.yr_constr)
		k = i+1

	for i, p in enumerate(msbuilding):
		worksheet.write(k+i+2,0, p.uniq)
		worksheet.write(k+i+2,1, p.bl_id)
		worksheet.write(k+i+2,2, p.addr)
		if p.ty_const == "Composite":
			worksheet.write(k+i+2,3, "Composite")
		else:
			worksheet.write(k+i+2,3, "Brick Masonary")
		worksheet.write(k+i+2,4, p.no_floor)
		worksheet.write(k+i+2,5, p.gps_x)
		worksheet.write(k+i+2,6, p.gps_y)
		worksheet.write(k+i+2,7, p.oc_day)
		worksheet.write(k+i+2,8, p.oc_night)
		worksheet.write(k+i+2,9, p.perf_score)
		worksheet.write(k+i+2,10, p.bas_prsnt)
		worksheet.write(k+i+2,11, p.hvy_ovh)
		worksheet.write(k+i+2,12, p.pnding)
		worksheet.write(k+i+2,13, p.yr_constr)
		k2 = k+i+1

	for i, p in enumerate(hybuilding):
		worksheet.write(k2+i+2,0, p.uniq)
		worksheet.write(k2+i+2,1, p.bl_id)
		worksheet.write(k2+i+2,2, p.addr)
		worksheet.write(k2+i+2,3, "Composite")
		worksheet.write(k2+i+2,4, p.no_floor)
		worksheet.write(k2+i+2,5, p.gps_x)
		worksheet.write(k2+i+2,6, p.gps_y)
		worksheet.write(k2+i+2,7, p.oc_day)
		worksheet.write(k2+i+2,8, p.oc_night)
		worksheet.write(k2+i+2,9, p.perf_score)
		worksheet.write(k2+i+2,10, p.bas_prsnt)
		worksheet.write(k2+i+2,11, p.hvy_ovh)
		worksheet.write(k2+i+2,12, p.pnding)
		worksheet.write(k2+i+2,13, p.yr_constr)

	worksheet2 = workbook.add_worksheet("Sheet2")
	bas_cnt = 0
	ovh_cnt = 0
	pnd_cnt = 0
	total_cnt = RC_Building.objects.all().count() + MS_Building.objects.all().count() + HY_Building.objects.all().count()
	for i,p in enumerate(rcbuilding):
		if p.bas_prsnt is 1:
			bas_cnt = bas_cnt + 1
		if p.hvy_ovh is 1:
			ovh_cnt = ovh_cnt + 1
		if p.pnding is 1:
			pnd_cnt = pnd_cnt + 1

	for i,p in enumerate(msbuilding):
		if p.bas_prsnt is 1:
			bas_cnt = bas_cnt + 1
		if p.hvy_ovh is 1:
			ovh_cnt = ovh_cnt + 1
		if p.pnding is 1:
			pnd_cnt = pnd_cnt + 1

	for i,p in enumerate(hybuilding):
		if p.bas_prsnt is 1:
			bas_cnt = bas_cnt + 1
		if p.hvy_ovh is 1:
			ovh_cnt = ovh_cnt + 1
		if p.pnding is 1:
			pnd_cnt = pnd_cnt + 1

	worksheet2.write(0,0, "Basements", bold)
	worksheet2.write(1,0, "Total", bold)
	worksheet2.write(1,1, total_cnt)
	worksheet2.write(2,0, "Present")
	worksheet2.write(2,1, bas_cnt)
	worksheet2.write(3,0, "Absent")
	worksheet2.write(3,1, total_cnt - bas_cnt)

	worksheet2.write(6,0, "Heavy Overhangs", bold)
	worksheet2.write(7,0, "Total", bold)
	worksheet2.write(7,1, total_cnt)
	worksheet2.write(8,0, "Present")
	worksheet2.write(8,1, ovh_cnt)
	worksheet2.write(9,0, "Absent")
	worksheet2.write(9,1, total_cnt - ovh_cnt)

	worksheet2.write(12,0, "Pounding", bold)
	worksheet2.write(13,0, "Total", bold)
	worksheet2.write(13,1, total_cnt)
	worksheet2.write(14,0, "Present")
	worksheet2.write(14,1, pnd_cnt)
	worksheet2.write(15,0, "Absent")
	worksheet2.write(15,1, total_cnt - pnd_cnt)	

	workbook.close()
	filename = 'RVS.xlsx'
	output.seek(0)
	response = HttpResponse(output.read(), content_type="application/ms-excel")
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response

@staff_member_required
def RCExcel(request):
	rcbuilding = RC_Building.objects.all().order_by('uniq')
	output = StringIO.StringIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet('Sheet1')
	date_format = workbook.add_format({'num_format':'mmmm dd yyyy'})
	worksheet.write(0, 0, "Generated:")
	generated = strftime("%d-%m-%Y %H:%M:%S IST", localtime())
	worksheet.write(0,1, generated)
	worksheet.write(0,4, "RC Buildings")
	worksheet.write(0,6, "Total:")
	rc_cnt = RC_Building.objects.all().count()
	worksheet.write(0,7, rc_cnt)
	bold = workbook.add_format({'bold': True})

	worksheet.write(1,0, "Unique ID", bold)
	worksheet.write(1,1, "Building ID", bold)
	worksheet.write(1,2, "Address", bold)
	worksheet.write(1,3, "Type", bold)
	worksheet.write(1,4, "No. of Floors", bold)
	worksheet.write(1,5, "GPS X", bold)
	worksheet.write(1,6, "GPS Y", bold)
	worksheet.write(1,7, "Day Occupancy", bold)
	worksheet.write(1,8, "Night Occupancy", bold)
	worksheet.write(1,9, "RVS Score", bold)
	worksheet.write(1,10, "Soft Storey", bold)
	worksheet.write(1,11, "Vertical Irregularity", bold)
	worksheet.write(1,12, "Plan Irregualrity", bold)
	worksheet.write(1,13, "Heavy Overhangs", bold)
	worksheet.write(1,14, "Short Column", bold)
	worksheet.write(1,15, "Apparent Quality", bold)
	worksheet.write(1,16, "Pounding", bold)
	worksheet.write(1,17, "Basement", bold)

	for i, p in enumerate(rcbuilding):
		worksheet.write(i+2,0, p.uniq)
		worksheet.write(i+2,1, p.bl_id)
		worksheet.write(i+2,2, p.addr)
		worksheet.write(i+2,3, "RC")
		worksheet.write(i+2,4, p.no_floor)
		worksheet.write(i+2,5, p.gps_x)
		worksheet.write(i+2,6, p.gps_y)
		worksheet.write(i+2,7, p.oc_day)
		worksheet.write(i+2,8, p.oc_night)
		worksheet.write(i+2,9, p.perf_score)
		worksheet.write(i+2,10, p.soft_st)
		worksheet.write(i+2,11, p.vrt_irr)
		worksheet.write(i+2,12, p.pl_irr)
		worksheet.write(i+2,13, p.hvy_ovh)
		worksheet.write(i+2,14, p.shr_col)
		worksheet.write(i+2,15, p.ap_qlt)
		worksheet.write(i+2,16, p.pnding)
		worksheet.write(i+2,17, p.bas_prsnt)
	
	worksheet2 = workbook.add_worksheet("Sheet2")
	total_cnt = RC_Building.objects.all().count()


	workbook.close()
	filename = 'RC-Excel.xlsx'
	output.seek(0)
	response = HttpResponse(output.read(), content_type="application/ms-excel")
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response

@staff_member_required
def MSExcel(request):
	msbuilding = MS_Building.objects.all().order_by('uniq')
	output = StringIO.StringIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet('Sheet1')
	date_format = workbook.add_format({'num_format':'mmmm dd yyyy'})
	worksheet.write(0, 0, "Generated:")
	generated = strftime("%d-%m-%Y %H:%M:%S IST", localtime())
	worksheet.write(0,1, generated)
	worksheet.write(0,4, "Masonary Buildings")
	worksheet.write(0,6, "Total:")
	ms_cnt = MS_Building.objects.all().count()
	worksheet.write(0,7, ms_cnt)
	bold = workbook.add_format({'bold': True})

	worksheet.write(1,0, "Unique ID", bold)
	worksheet.write(1,1, "Building ID", bold)
	worksheet.write(1,2, "Address", bold)
	worksheet.write(1,3, "Type", bold)
	worksheet.write(1,4, "No. of Floors", bold)
	worksheet.write(1,5, "GPS X", bold)
	worksheet.write(1,6, "GPS Y", bold)
	worksheet.write(1,7, "Day Occupancy", bold)
	worksheet.write(1,8, "Night Occupancy", bold)
	worksheet.write(1,9, "RVS Score", bold)
	worksheet.write(1,10, "Structural Irregularity", bold)
	worksheet.write(1,11, "Heavy Overhangs", bold)
	worksheet.write(1,12, "Irregular Openings", bold)
	worksheet.write(1,13, "Apparent Quality", bold)
	worksheet.write(1,14, "Pounding", bold)
	worksheet.write(1,15, "Opening Size", bold)
	worksheet.write(1,16, "Horizontal Bands", bold)
	worksheet.write(1,17, "Basement", bold)
	worksheet.write(1,18, "Type of Construction", bold)

	for i, p in enumerate(msbuilding):
		worksheet.write(i+2,0, p.uniq)
		worksheet.write(i+2,1, p.bl_id)
		worksheet.write(i+2,2, p.addr)
		worksheet.write(i+2,3, "Masonary")
		worksheet.write(i+2,4, p.no_floor)
		worksheet.write(i+2,5, p.gps_x)
		worksheet.write(i+2,6, p.gps_y)
		worksheet.write(i+2,7, p.oc_day)
		worksheet.write(i+2,8, p.oc_night)
		worksheet.write(i+2,9, p.perf_score)
		worksheet.write(i+2,10, p.str_irr)
		worksheet.write(i+2,11, p.hvy_ovh)
		worksheet.write(i+2,12, p.irr_opn)
		worksheet.write(i+2,13, p.ap_qlt)
		worksheet.write(i+2,14, p.pnding)
		worksheet.write(i+2,15, p.prt_opn)
		worksheet.write(i+2,16, p.hrz_bnd)
		worksheet.write(i+2,17, p.bas_prsnt)
		worksheet.write(i+2,18, p.ty_const)

	workbook.close()
	filename = 'MS-Excel.xlsx'
	output.seek(0)
	response = HttpResponse(output.read(), content_type="application/ms-excel")
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response

@staff_member_required
def HYExcel(request):
	hybuilding = HY_Building.objects.all().order_by('uniq')
	output = StringIO.StringIO()
	workbook = xlsxwriter.Workbook(output)
	worksheet = workbook.add_worksheet('Sheet1')
	date_format = workbook.add_format({'num_format':'mmmm dd yyyy'})
	worksheet.write(0, 0, "Generated:")
	generated = strftime("%d-%m-%Y %H:%M:%S IST", localtime())
	worksheet.write(0,1, generated)
	worksheet.write(0,4, "Composite Buildings")
	worksheet.write(0,6, "Total:")
	hy_cnt = HY_Building.objects.all().count()
	worksheet.write(0,7, hy_cnt)
	bold = workbook.add_format({'bold': True})

	worksheet.write(1,0, "Unique ID", bold)
	worksheet.write(1,1, "Building ID", bold)
	worksheet.write(1,2, "Address", bold)
	worksheet.write(1,3, "Type", bold)
	worksheet.write(1,4, "No. of Floors", bold)
	worksheet.write(1,5, "GPS X", bold)
	worksheet.write(1,6, "GPS Y", bold)
	worksheet.write(1,7, "Day Occupancy", bold)
	worksheet.write(1,8, "Night Occupancy", bold)
	worksheet.write(1,9, "RVS Score", bold)
	worksheet.write(1,10, "Structural Irregularity", bold)
	worksheet.write(1,11, "Heavy Overhangs", bold)
	worksheet.write(1,12, "Irregular Openings", bold)
	worksheet.write(1,13, "Apparent Quality", bold)
	worksheet.write(1,14, "Pounding", bold)
	worksheet.write(1,15, "Opening Size", bold)
	worksheet.write(1,16, "Horizontal Bands", bold)
	worksheet.write(1,17, "Hybrid Action", bold)
	worksheet.write(1,18, "Basement", bold)

	for i, p in enumerate(hybuilding):
		worksheet.write(i+2,0, p.uniq)
		worksheet.write(i+2,1, p.bl_id)
		worksheet.write(i+2,2, p.addr)
		worksheet.write(i+2,3, "Composite")
		worksheet.write(i+2,4, p.no_floor)
		worksheet.write(i+2,5, p.gps_x)
		worksheet.write(i+2,6, p.gps_y)
		worksheet.write(i+2,7, p.oc_day)
		worksheet.write(i+2,8, p.oc_night)
		worksheet.write(i+2,9, p.perf_score)
		worksheet.write(i+2,10, p.str_irr)
		worksheet.write(i+2,11, p.hvy_ovh)
		worksheet.write(i+2,12, p.irr_opn)
		worksheet.write(i+2,13, p.ap_qlt)
		worksheet.write(i+2,14, p.pnding)
		worksheet.write(i+2,15, p.prt_opn)
		worksheet.write(i+2,16, p.hrz_bnd)
		worksheet.write(i+2,17, p.hyb_act)
		worksheet.write(i+2,18, p.bas_prsnt)

	workbook.close()
	filename = 'HY-Excel.xlsx'
	output.seek(0)
	response = HttpResponse(output.read(), content_type="application/ms-excel")
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response