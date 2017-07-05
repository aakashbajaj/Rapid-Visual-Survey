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
	worksheet = workbook.add_worksheet('New-SpreadSheet')
	date_format = workbook.add_format({'num_format':'mmmm dd yyyy'})
	worksheet.write(0, 0, "Generated:")
	generated = strftime("%d-%m-%Y %H:%M:%S IST/India", localtime())
	worksheet.write(0,1, generated)

	worksheet.write(1,0, "Unique ID")
	worksheet.write(1,1, "Building ID")
	worksheet.write(1,2, "Address")
	worksheet.write(1,3, "Type")
	worksheet.write(1,4, "No. of Floors")
	worksheet.write(1,5, "GPS X")
	worksheet.write(1,6, "GPS Y")
	worksheet.write(1,7, "Day Occupancy")
	worksheet.write(1,8, "Night Occupancy")
	worksheet.write(1,9, "RVS Score")

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
		k = i+1

	for i, p in enumerate(msbuilding):
		worksheet.write(k+i+2,0, p.uniq)
		worksheet.write(k+i+2,1, p.bl_id)
		worksheet.write(k+i+2,2, p.addr)
		worksheet.write(k+i+2,3, "Masonary")
		worksheet.write(k+i+2,4, p.no_floor)
		worksheet.write(k+i+2,5, p.gps_x)
		worksheet.write(k+i+2,6, p.gps_y)
		worksheet.write(k+i+2,7, p.oc_day)
		worksheet.write(k+i+2,8, p.oc_night)
		worksheet.write(k+i+2,9, p.perf_score)
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
	worksheet = workbook.add_worksheet('New-SpreadSheet')
	date_format = workbook.add_format({'num_format':'mmmm dd yyyy'})
	worksheet.write(0, 0, "Generated:")
	generated = strftime("%d-%m-%Y %H:%M:%S IST/India", localtime())
	worksheet.write(0,1, generated)
	worksheet.write(0,2, "RC Buildings")

	worksheet.write(1,0, "Unique ID")
	worksheet.write(1,1, "Building ID")
	worksheet.write(1,2, "Address")
	worksheet.write(1,3, "Type")
	worksheet.write(1,4, "No. of Floors")
	worksheet.write(1,5, "GPS X")
	worksheet.write(1,6, "GPS Y")
	worksheet.write(1,7, "Day Occupancy")
	worksheet.write(1,8, "Night Occupancy")
	worksheet.write(1,9, "RVS Score")
	worksheet.write(1,10, "Soft Storey")
	worksheet.write(1,11, "Vertical Irregularity")
	worksheet.write(1,12, "Plan Irregualrity")
	worksheet.write(1,13, "Heavy Overhangs")
	worksheet.write(1,14, "Short Column")
	worksheet.write(1,15, "Apparent Quality")
	worksheet.write(1,16, "Pounding")

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
	worksheet = workbook.add_worksheet('New-SpreadSheet')
	date_format = workbook.add_format({'num_format':'mmmm dd yyyy'})
	worksheet.write(0, 0, "Generated:")
	generated = strftime("%d-%m-%Y %H:%M:%S IST/India", localtime())
	worksheet.write(0,1, generated)
	worksheet.write(0,2, "Masonary Buildings")

	worksheet.write(1,0, "Unique ID")
	worksheet.write(1,1, "Building ID")
	worksheet.write(1,2, "Address")
	worksheet.write(1,3, "Type")
	worksheet.write(1,4, "No. of Floors")
	worksheet.write(1,5, "GPS X")
	worksheet.write(1,6, "GPS Y")
	worksheet.write(1,7, "Day Occupancy")
	worksheet.write(1,8, "Night Occupancy")
	worksheet.write(1,9, "RVS Score")
	worksheet.write(1,10, "Structural Irregularity")
	worksheet.write(1,11, "Heavy Overhangs")
	worksheet.write(1,12, "Irregular Openings")
	worksheet.write(1,13, "Apparent Quality")
	worksheet.write(1,14, "Pounding")
	worksheet.write(1,15, "Opening Size")
	worksheet.write(1,16, "Horizontal Bands")

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
	worksheet = workbook.add_worksheet('New-SpreadSheet')
	date_format = workbook.add_format({'num_format':'mmmm dd yyyy'})
	worksheet.write(0, 0, "Generated:")
	generated = strftime("%d-%m-%Y %H:%M:%S IST/India", localtime())
	worksheet.write(0,1, generated)
	worksheet.write(0,2, "Composite Buildings")

	worksheet.write(1,0, "Unique ID")
	worksheet.write(1,1, "Building ID")
	worksheet.write(1,2, "Address")
	worksheet.write(1,3, "Type")
	worksheet.write(1,4, "No. of Floors")
	worksheet.write(1,5, "GPS X")
	worksheet.write(1,6, "GPS Y")
	worksheet.write(1,7, "Day Occupancy")
	worksheet.write(1,8, "Night Occupancy")
	worksheet.write(1,9, "RVS Score")
	worksheet.write(1,10, "Structural Irregularity")
	worksheet.write(1,11, "Heavy Overhangs")
	worksheet.write(1,12, "Irregular Openings")
	worksheet.write(1,13, "Apparent Quality")
	worksheet.write(1,14, "Pounding")
	worksheet.write(1,15, "Opening Size")
	worksheet.write(1,16, "Horizontal Bands")
	worksheet.write(1,17, "Hybrid Action")

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

	workbook.close()
	filename = 'HY-Excel.xlsx'
	output.seek(0)
	response = HttpResponse(output.read(), content_type="application/ms-excel")
	response['Content-Disposition'] = 'attachment; filename=%s' % filename
	return response