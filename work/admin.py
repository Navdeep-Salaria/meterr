from django.contrib import admin
from .models import Meter, SolarMeter

@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ['meter_id', 'total_energy_wh', 'current_power_w', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['meter_id']
    readonly_fields = ['last_updated']
    fieldsets = (
        ('Meter Information', {
            'fields': ('meter_id',)
        }),
        ('Readings', {
            'fields': ('total_energy_wh', 'current_power_w', 'last_updated')
        }),
    )

@admin.register(SolarMeter)
class SolarMeterAdmin(admin.ModelAdmin):
    list_display = ['meter_id', 'total_energy_wh', 'current_power_w', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['meter_id']
    readonly_fields = ['last_updated']
    fieldsets = (
        ('Meter Information', {
            'fields': ('meter_id',)
        }),
        ('Readings', {
            'fields': ('total_energy_wh', 'current_power_w', 'last_updated')
        }),
    )
