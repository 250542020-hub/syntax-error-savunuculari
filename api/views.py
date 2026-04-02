from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SensorData  # Gereksiz ikinci importu sildik
from .analysis import TarimAnalizMotoru

class IstatistikselAnaliz(APIView):
    def get(self, request):
        # Son 100 veriyi çekelim
        queryset = SensorData.objects.all().order_by('-timestamp')[:100]
        
        if not queryset.exists():
            return Response({"hata": "Analiz için yeterli veri yok."}, status=404)

        # Verileri listeye çevir
        nem_verileri = [obj.soil_moisture for obj in queryset]
        sicaklik_verileri = [obj.temperature for obj in queryset]

        # Analiz Motorunu Çalıştır
        nem_sonuc = TarimAnalizMotoru.analiz_et(nem_verileri)
        sicaklik_sonuc = TarimAnalizMotoru.analiz_et(sicaklik_verileri)

        return Response({
            "toprak_nemi_analizi": nem_sonuc,
            "sicaklik_analizi": sicaklik_sonuc
        })

class SensorDataReceiver(APIView):
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
