import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.validators import sensor_verisini_dogrula, hava_durumu_cevabini_dogrula, genel_cevap_dogrula

def baslik(s): print("\n" + "="*55 + f"\n  {s}\n" + "="*55)
def sonuc(ad, beklenen, s):
    durum = "GECTI" if s["gecerli"] == beklenen else "BASARISIZ"
    print(f"\n  [{durum}] {ad}")
    if s["hatalar"]: print(f"         Hatalar  : {s['hatalar']}")
    if s["uyarilar"]: print(f"         Uyarilar : {s['uyarilar']}")

baslik("TEST 1 - Sensor Verisi Dogrulama")
sonuc("Gecerli veri", True,  sensor_verisini_dogrula({"device_id":"SENSOR_01","temperature":25.5,"humidity":55.0,"soil_moisture":45.0}))
sonuc("Eksik alan",   False, sensor_verisini_dogrula({"device_id":"SENSOR_02","temperature":28.0}))
sonuc("Aralik disi sicaklik (150)", False, sensor_verisini_dogrula({"device_id":"SENSOR_03","temperature":150.0,"humidity":70.0,"soil_moisture":35.0}))
sonuc("Negatif nem (-5)", False, sensor_verisini_dogrula({"device_id":"SENSOR_04","temperature":22.0,"humidity":-5.0,"soil_moisture":40.0}))
sonuc("Dusuk toprak nemi - uyari uretmeli", True, sensor_verisini_dogrula({"device_id":"SENSOR_05","temperature":30.0,"humidity":45.0,"soil_moisture":10.0}))
sonuc("Yanlis tip (sicaklik metin)", False, sensor_verisini_dogrula({"device_id":"SENSOR_06","temperature":"sicak","humidity":60.0,"soil_moisture":35.0}))
sonuc("Bos device_id", False, sensor_verisini_dogrula({"device_id":"","temperature":24.0,"humidity":55.0,"soil_moisture":40.0}))

baslik("TEST 2 - Hava Durumu API Dogrulama")
sonuc("Gecerli hava durumu", True,  hava_durumu_cevabini_dogrula({"city":"Elazig","temperature":22.0,"humidity":60.0,"description":"Parcali bulutlu"}))
sonuc("Eksik sehir bilgisi", False, hava_durumu_cevabini_dogrula({"temperature":25.0,"humidity":50.0,"description":"Gunesli"}))
sonuc("Sicaklik aralik disi (90)", False, hava_durumu_cevabini_dogrula({"city":"Ankara","temperature":90.0,"humidity":40.0,"description":"Gunesli"}))

baslik("TEST 3 - HTTP Durum Kodu Dogrulama")
for kod, beklenen in [(200,True),(400,False),(401,False),(404,False),(429,True),(500,False)]:
    sonuc(f"HTTP {kod}", beklenen, genel_cevap_dogrula({}, kod))

print("\n" + "="*55)
print("  Tum testler tamamlandi.")
print("="*55 + "\n")
