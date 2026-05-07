from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token
from api.views import SensorDataReceiver, IstatistikselAnaliz

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpointleri
    path('api/sensor-data/', SensorDataReceiver.as_view(), name='sensor_data'),
    path('api/analysis/', IstatistikselAnaliz.as_view(), name='istatistik_analiz'),
    path('api/token/', obtain_auth_token, name='api_token_al'),  # IoT cihazlar buradan token alacak

    # Login / Logout (web arayuzu icin)
    path('giris/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('cikis/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard (en altta kalmali — '' her seyi yakalar)
    path('', include('dashboard.urls')),
]