from rest_framework import serializers
from .models import Meter, SolarMeter

class MeterSerializer(serializers.ModelSerializer):
    total_energy_kwh = serializers.SerializerMethodField()
    
    class Meta:
        model = Meter
        fields = ['meter_id', 'total_energy_kwh', 'current_power_w', 'last_updated']
        read_only_fields = ['meter_id', 'last_updated']
    
    def get_total_energy_kwh(self, obj):
        return round((obj.total_energy_wh or 0) / 1000.0, 3)
    
    def update(self, instance, validated_data):
        # Handle total_energy_kwh from input
        if 'total_energy_kwh' in self.initial_data:
            kwh = float(self.initial_data['total_energy_kwh'])
            instance.total_energy_wh = int(round(kwh * 1000))
        if 'current_power_w' in validated_data:
            instance.current_power_w = validated_data['current_power_w']
        instance.save()
        return instance


class SolarMeterSerializer(serializers.ModelSerializer):
    total_energy_kwh = serializers.SerializerMethodField()
    
    class Meta:
        model = SolarMeter
        fields = ['meter_id', 'total_energy_kwh', 'current_power_w', 'last_updated']
        read_only_fields = ['meter_id', 'last_updated']
    
    def get_total_energy_kwh(self, obj):
        return round((obj.total_energy_wh or 0) / 1000.0, 3)
    
    def update(self, instance, validated_data):
        # Handle total_energy_kwh from input - ALWAYS update
        if 'total_energy_kwh' in self.initial_data:
            kwh = float(self.initial_data['total_energy_kwh'])
            instance.total_energy_wh = int(round(kwh * 1000))
            print(f"✅ Solar DRF: Updating energy to {instance.total_energy_wh}Wh ({kwh:.3f} kWh)")
        if 'current_power_w' in validated_data:
            instance.current_power_w = validated_data['current_power_w']
        instance.save()
        return instance
