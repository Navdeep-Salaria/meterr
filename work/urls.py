from django.urls import path
from .views import meter_page, solar_page, MeterAPIView, SolarMeterAPIView

urlpatterns = [
    path('', meter_page, name='meter_page'),
    path('meter/', MeterAPIView.as_view(), name='meter_api'),
    path('api/meter/', MeterAPIView.as_view(), name='meter_api_alt'),
    path('solar/ui/', solar_page, name='solar_page'),
    path('solar/', SolarMeterAPIView.as_view(), name='solar_api'),
]
