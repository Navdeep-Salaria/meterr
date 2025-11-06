from django.shortcuts import render
from .models import Meter, SolarMeter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import MeterSerializer, SolarMeterSerializer
from django.utils import timezone

def meter_page(request):
    return render(request, 'work/index.html')

def solar_page(request):
    return render(request, 'work/solar.html')


class MeterAPIView(APIView):
    """
    API endpoint for main meter - GET returns current values, POST updates values
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # Disable authentication
    
    def get(self, request):
        meter, created = Meter.objects.get_or_create(
            meter_id='main',
            defaults={'total_energy_wh': 0, 'current_power_w': 0}
        )
        meter.refresh_from_db()
        serializer = MeterSerializer(meter)
        data = serializer.data
        data['timestamp'] = timezone.now().isoformat()
        data['status'] = 'active'
        return Response(data)
    
    def post(self, request):
        print(f"Meter POST received: {request.data}")
        meter, created = Meter.objects.get_or_create(
            meter_id='main',
            defaults={'total_energy_wh': 0, 'current_power_w': 0}
        )
        
        old_energy = meter.total_energy_wh
        old_power = meter.current_power_w
        
        # METER → DATABASE: Update from request data - ALWAYS update, no restrictions
        if 'total_energy_kwh' in request.data:
            kwh = float(request.data['total_energy_kwh'])
            new_wh = int(round(kwh * 1000))
            meter.total_energy_wh = new_wh
            print(f"Meter -> Database: Updating energy from {old_energy}Wh -> {new_wh}Wh ({kwh:.3f} kWh)")
        
        if 'current_power_w' in request.data:
            new_power = int(round(float(request.data['current_power_w'])))
            meter.current_power_w = new_power
            print(f"Meter -> Database: Updating power from {old_power}W -> {new_power}W")
        
        # Save to database
        meter.save()
        meter.refresh_from_db()
        print(f"Database updated: {meter.total_energy_wh}Wh ({meter.total_energy_wh/1000.0:.3f} kWh), {meter.current_power_w}W (ID: {meter.id})")
        
        # DATABASE → API: Return updated JSON
        serializer = MeterSerializer(meter)
        data = serializer.data
        data['timestamp'] = timezone.now().isoformat()
        data['status'] = 'active'
        print(f"API returning JSON: {data}")
        return Response(data)


class SolarMeterAPIView(APIView):
    """
    API endpoint for solar meter - GET returns current values, POST updates values
    """
    permission_classes = [AllowAny]
    authentication_classes = []  # Disable authentication
    
    def get(self, request):
        smeter, created = SolarMeter.objects.get_or_create(
            meter_id='solar',
            defaults={'total_energy_wh': 0, 'current_power_w': 0}
        )
        smeter.refresh_from_db()
        serializer = SolarMeterSerializer(smeter)
        data = serializer.data
        data['timestamp'] = timezone.now().isoformat()
        data['status'] = 'active'
        return Response(data)
    
    def post(self, request):
        print(f"Solar POST received: {request.data}")
        smeter, created = SolarMeter.objects.get_or_create(
            meter_id='solar',
            defaults={'total_energy_wh': 0, 'current_power_w': 0}
        )
        
        old_energy = smeter.total_energy_wh
        old_power = smeter.current_power_w
        
        # Update from request data - ALWAYS update
        updated = False
        if 'total_energy_kwh' in request.data:
            kwh = float(request.data['total_energy_kwh'])
            new_wh = int(round(kwh * 1000))
            smeter.total_energy_wh = new_wh
            updated = True
            print(f"OK Solar: Updating energy from {old_energy}Wh -> {new_wh}Wh ({kwh:.3f} kWh)")
        
        if 'current_power_w' in request.data:
            new_power = int(round(float(request.data['current_power_w'])))
            smeter.current_power_w = new_power
            updated = True
            print(f"OK Solar: Updating power from {old_power}W -> {new_power}W")
        
        if updated:
            smeter.save()
            smeter.refresh_from_db()
            print(f"OK Solar SAVED TO DB: {smeter.total_energy_wh}Wh ({smeter.total_energy_wh/1000.0:.3f} kWh), {smeter.current_power_w}W (ID: {smeter.id})")
        else:
            print(f"WARNING Solar: No updates in request data")
        
        serializer = SolarMeterSerializer(smeter)
        data = serializer.data
        data['timestamp'] = timezone.now().isoformat()
        data['status'] = 'active'
        print(f"Solar API returning: {data}")
        return Response(data)
