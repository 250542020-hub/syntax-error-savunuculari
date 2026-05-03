from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions # İzinler eklendi
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .models import SensorData
from .analysis import TarimAnalizMotoru

class IstatistikselAnaliz(APIView):
    # Sadece giriş yapmış kullanıcılar verileri görebilir
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = SensorData.objects.all().order_by('-timestamp')[:100]
        
        if not queryset.exists():
            return Response({"hata": "Analiz için yeterli veri yok."}, status=status.HTTP_404_NOT_FOUND)

        nem_verileri = [obj.soil_moisture for obj in queryset]
        sicaklik_verileri = [obj.temperature for obj in queryset]

        nem_sonuc = TarimAnalizMotoru.analiz_et(nem_verileri)
        sicaklik_sonuc = TarimAnalizMotoru.analiz_et(sicaklik_verileri)

        return Response({
            "toprak_nemi_analizi": nem_sonuc,
            "sicaklik_analizi": sicaklik_sonuc
        })

class SensorDataReceiver(APIView):
    # Veri göndermek için de yetki şart (Güvenlik önlemi)
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            data = request.data
            new_record = SensorData.objects.create(
                device_id=data.get('device_id'),
                temperature=data.get('temperature'),
                humidity=data.get('humidity'),
                soil_moisture=data.get('soil_moisture')
            )

            soil_moisture = float(data.get('soil_moisture', 100))
            action = "DURUM: Nem ideal. İşlem gerekmiyor. 🌾"
            if soil_moisture < 30:
                action = "KRİTİK: Toprak kuru! Sulama sistemi başlatıldı. ✅"
            elif soil_moisture > 70:
                action = "UYARI: Toprak doygun. Sulama durduruldu. 🛑"

            return Response({
                "mesaj": "Veri başarıyla işlendi",
                "karar": action,
                "kayit_id": new_record.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"hata": "Veri formatı hatalı veya eksik."}, status=status.HTTP_400_BAD_REQUEST)