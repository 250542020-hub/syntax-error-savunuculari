from django.contrib import admin
from .models import SensorData

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'temperature', 'humidity', 'soil_moisture', 'timestamp')
    list_filter = ('device_id', 'timestamp')