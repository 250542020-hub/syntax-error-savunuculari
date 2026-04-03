from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('sensorler/', views.sensor_listesi, name='sensor_listesi'),
    path('sensor-ekle/', views.sensor_ekle, name='sensor_ekle'),
    path('sensor-sil/<str:device_id>/', views.sensor_sil, name='sensor_sil'),
]