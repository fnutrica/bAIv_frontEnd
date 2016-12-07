from django.contrib import admin

# Register your models here.

from .models import Player, Scenario, Input

admin.site.register(Player)
admin.site.register(Scenario)
admin.site.register(Input)