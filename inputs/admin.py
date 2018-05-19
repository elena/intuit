# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Sale, Hour


admin.site.register(Sale)
admin.site.register(Hour)
