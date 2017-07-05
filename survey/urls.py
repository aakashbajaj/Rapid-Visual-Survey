from django.conf.urls import url
from django.contrib import admin

from views import *


urlpatterns = [
	url(r'^$', index, name='index'),
	url(r'^excel/all$', BuildingExcel, name='excel'),
	url(r'^excel/rc$', RCExcel, name='rcexcel'),
	url(r'^excel/ms$', MSExcel, name='msexcel'),
	url(r'^excel/hy$', HYExcel, name='hyexcel')
]