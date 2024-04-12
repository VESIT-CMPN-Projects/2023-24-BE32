# dashboard/admin.py
from django.contrib import admin
from .models import PollingData, History

admin.site.register(PollingData)
admin.site.register(History)
