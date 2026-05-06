import os
import time
# Django ortamını ayarlamadan sadece motoru test edelim
from api.analysis import TarimAnalizMotoru

# Test Verisi (10.000 adet rastgele sensör verisi simüle edelim)
test_verisi = [float(x) for x in range(1, 10001)] # 1'den 10.000'e kadar

print("🚀 TensorFlow Analiz Testi Başlıyor...")
baslangic = time.time()

sonuclar = TarimAnalizMotoru.analiz_et(test_verisi)

bitis = time.time()

print(f"✅ Analiz Tamamlandı! Süre: {bitis - baslangic:.4f} saniye")
print(f"📊 Ortalama: {sonuclar['ortalama']}")
print(f"📊 Medyan: {sonuclar['medyan']}")
print(f"📊 Std Sapma: {sonuclar['standart_sapma']}")

# Doğruluk Kontrolü
beklenen_ortalama = 5000.5
if abs(sonuclar['ortalama'] - beklenen_ortalama) < 0.01:
    print("🎯 Hesaplama Doğruluğu: Mükemmel")