from django.contrib import admin

# Register your models here.

from .models import Scenario, Input

admin.site.register(Scenario)
admin.site.register(Input)