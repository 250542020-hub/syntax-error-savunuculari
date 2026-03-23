from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SensorData

class SensorDataReceiver(APIView):
    def post(self, request):
        try:
            # Gelen JSON verisini alalım
            data = request.data
            
            # Veritabanına kaydedelim
            new_record = SensorData.objects.create(
                device_id=data.get('device_id'),
                temperature=data.get('temperature'),
                humidity=data.get('humidity'),
                soil_moisture=data.get('soil_moisture')
            )

            # Basit Akıllı Karar Mekanizması
            soil_moisture = float(data.get('soil_moisture', 100))
            if soil_moisture < 30:
                action = "KRİTİK: Toprak kuru! Sulama sistemi başlatıldı. ✅"
            elif soil_moisture > 70:
                action = "UYARI: Toprak doygun. Sulama durduruldu. 🛑"
            else:
                action = "DURUM: Nem ideal. İşlem gerekmiyor. 🌾"

            return Response({
                "mesaj": "Veri başarıyla işlendi",
                "karar": action,
                "kayit_id": new_record.id
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"hata": str(e)}, status=status.HTTP_400_BAD_REQUEST)