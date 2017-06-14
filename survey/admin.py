# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import RC_Building, Team
# Register your models here.

admin.site.register(RC_Building)
admin.site.register(Team)

# admin.site.unregister(Building)
# admin.site.unregister(RC)
# admin.site.unregister(Team)

