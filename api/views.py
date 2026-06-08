import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions  # İzinler eklendi
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.db import OperationalError, InterfaceError  # DB baglanti hatalari
from .models import SensorData
from .analysis import TarimAnalizMotoru
from .validators import sensor_verisini_dogrula

logger = logging.getLogger("api.views")

# ─────────────────────────────────────────────
# Sulama kararı tek bir yerde tanımlandı.
# Daha önce bu mantık views.py içine gömülüydü,
# validators.py'deki eşiklerle çakışıyordu.
# ─────────────────────────────────────────────
def sulama_karari_uret(soil_moisture: float) -> str:
    if soil_moisture < 30:
        return "KRİTİK: Toprak kuru! Sulama sistemi başlatıldı. ✅"
    elif soil_moisture > 70:
        return "UYARI: Toprak doygun. Sulama durduruldu. 🛑"
    return "DURUM: Nem ideal. İşlem gerekmiyor. 🌾"


class IstatistikselAnaliz(APIView):
    # Sadece giriş yapmış kullanıcılar verileri görebilir
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            queryset = SensorData.objects.order_by('-timestamp')[:100]

            if not queryset.exists():
                return Response(
                    {"hata": "Analiz için yeterli veri yok."},
                    status=status.HTTP_404_NOT_FOUND
                )

            nem_verileri      = [obj.soil_moisture for obj in queryset]
            sicaklik_verileri = [obj.temperature   for obj in queryset]
        except (OperationalError, InterfaceError) as e:
            # DB baglantisi dustu/ulasilamiyor → 500 + stack trace yerine 503.
            logger.error("Analiz sirasinda DB baglanti hatasi: %s", e)
            return Response(
                {"hata": "Veritabanına şu an ulaşılamıyor. Lütfen daha sonra tekrar deneyin."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response({
            "toprak_nemi_analizi": TarimAnalizMotoru.analiz_et(nem_verileri),
            "sicaklik_analizi":    TarimAnalizMotoru.analiz_et(sicaklik_verileri),
        })


class SensorDataReceiver(APIView):
    # Veri göndermek için de yetki şart (Güvenlik önlemi)
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data

        # Doğrulama validators.py üzerinden yapılıyor (kod tekrarı önlendi)
        dogrulama = sensor_verisini_dogrula(data)
        if not dogrulama["gecerli"]:
            return Response(
                {"hata": "Geçersiz veri", "detaylar": dogrulama["hatalar"]},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            kayit = SensorData.objects.create(
                device_id     = data.get('device_id'),
                temperature   = data.get('temperature'),
                humidity      = data.get('humidity'),
                soil_moisture = data.get('soil_moisture'),
            )

            return Response({
                "mesaj":    "Veri başarıyla işlendi",
                "karar":    sulama_karari_uret(float(data.get('soil_moisture', 100))),
                "kayit_id": kayit.id,
                "uyarilar": dogrulama["uyarilar"],
            }, status=status.HTTP_201_CREATED)

        except (OperationalError, InterfaceError) as e:
            # DB baglanti hatasi: bu istemci hatasi (400) degil, gecici sunucu durumu (503).
            logger.error("Sensör verisi yazilirken DB baglanti hatasi: %s", e)
            return Response(
                {"hata": "Veritabanına şu an ulaşılamıyor. Lütfen daha sonra tekrar deneyin."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            # Generic hata mesaji - stack trace sizdirma riski yok
            return Response(
                {"hata": "Veri formatı hatalı veya eksik."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
