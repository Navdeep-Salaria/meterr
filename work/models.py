from django.db import models

class Meter(models.Model):
    meter_id = models.CharField(max_length=50, unique=True, default='main', help_text='Unique identifier for the meter')
    total_energy_wh = models.BigIntegerField(default=0, help_text='Total energy in watt-hours (integer)')
    current_power_w = models.IntegerField(default=0, help_text='Current power in watts (integer)')
    last_updated = models.DateTimeField(auto_now=True, help_text='Last update timestamp')

    class Meta:
        ordering = ['meter_id']
        verbose_name = 'Energy Meter'
        verbose_name_plural = 'Energy Meters'

    def __str__(self):
        kwh = (self.total_energy_wh or 0) / 1000.0
        return f"{self.meter_id}: {kwh:.3f} kWh ({self.current_power_w}W)"


class SolarMeter(models.Model):
    meter_id = models.CharField(max_length=50, unique=True, default='solar', help_text='Unique identifier for the solar meter')
    total_energy_wh = models.BigIntegerField(default=0, help_text='Total solar energy in watt-hours (integer)')
    current_power_w = models.IntegerField(default=0, help_text='Current solar power in watts (integer)')
    last_updated = models.DateTimeField(auto_now=True, help_text='Last update timestamp')

    class Meta:
        ordering = ['meter_id']
        verbose_name = 'Solar Energy Meter'
        verbose_name_plural = 'Solar Energy Meters'

    def __str__(self):
        kwh = (self.total_energy_wh or 0) / 1000.0
        return f"{self.meter_id}: {kwh:.3f} kWh ({self.current_power_w}W)"
