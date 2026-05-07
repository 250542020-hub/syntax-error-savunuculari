"""
tests.py — Akıllı Tarım Yönetim Sistemi
Kapsam: views.py, analysis.py, models.py, validators.py

Çalıştırmak için:
    python manage.py test api
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import SensorData
from .analysis import TarimAnalizMotoru
from .validators import sensor_verisini_dogrula, hava_durumu_cevabini_dogrula, genel_cevap_dogrula
from .views import sulama_karari_uret


# ══════════════════════════════════════════════════
# 1. MODEL TESTLERİ
# ══════════════════════════════════════════════════
class SensorDataModelTest(TestCase):

    def setUp(self):
        self.kayit = SensorData.objects.create(
            device_id="TEST_01",
            temperature=25.5,
            humidity=55.0,
            soil_moisture=40.0,
        )

    def test_kayit_olusturuldu(self):
        self.assertEqual(SensorData.objects.count(), 1)

    def test_str_temsili(self):
        self.assertIn("TEST_01", str(self.kayit))

    def test_timestamp_otomatik_eklendi(self):
        self.assertIsNotNone(self.kayit.timestamp)

    def test_alan_degerleri_dogru(self):
        self.assertEqual(self.kayit.temperature, 25.5)
        self.assertEqual(self.kayit.humidity, 55.0)
        self.assertEqual(self.kayit.soil_moisture, 40.0)


# ══════════════════════════════════════════════════
# 2. ANALİZ MOTORU TESTLERİ
# ══════════════════════════════════════════════════
class TarimAnalizMotoruTest(TestCase):

    def test_bos_liste(self):
        self.assertIsNone(TarimAnalizMotoru.analiz_et([]))

    def test_tek_eleman(self):
        sonuc = TarimAnalizMotoru.analiz_et([42.0])
        self.assertEqual(sonuc["ortalama"], 42.0)
        self.assertEqual(sonuc["medyan"],   42.0)
        self.assertEqual(sonuc["veri_adedi"], 1)

    def test_ortalama_dogru(self):
        sonuc = TarimAnalizMotoru.analiz_et([10.0, 20.0, 30.0])
        self.assertAlmostEqual(sonuc["ortalama"], 20.0, places=1)

    def test_medyan_tek_sayi(self):
        sonuc = TarimAnalizMotoru.analiz_et([1.0, 2.0, 3.0])
        self.assertAlmostEqual(sonuc["medyan"], 2.0, places=1)

    def test_medyan_cift_sayi(self):
        sonuc = TarimAnalizMotoru.analiz_et([1.0, 2.0, 3.0, 4.0])
        self.assertAlmostEqual(sonuc["medyan"], 2.5, places=1)

    def test_standart_sapma_sifir(self):
        sonuc = TarimAnalizMotoru.analiz_et([5.0, 5.0, 5.0])
        self.assertAlmostEqual(sonuc["standart_sapma"], 0.0, places=1)

    def test_veri_adedi_dogru(self):
        sonuc = TarimAnalizMotoru.analiz_et([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertEqual(sonuc["veri_adedi"], 5)


# ══════════════════════════════════════════════════
# 3. SULAMA KARARI TESTLERİ
# ══════════════════════════════════════════════════
class SulamaKarariTest(TestCase):

    def test_kritik_kuru(self):
        self.assertIn("Sulama sistemi başlatıldı", sulama_karari_uret(20.0))

    def test_doygun(self):
        self.assertIn("Sulama durduruldu", sulama_karari_uret(80.0))

    def test_ideal(self):
        self.assertIn("İşlem gerekmiyor", sulama_karari_uret(50.0))

    def test_sinir_deger_30(self):
        # 30 kritik değil, ideal
        self.assertIn("İşlem gerekmiyor", sulama_karari_uret(30.0))

    def test_sinir_deger_70(self):
        # 70 doygun değil, ideal
        self.assertIn("İşlem gerekmiyor", sulama_karari_uret(70.0))


# ══════════════════════════════════════════════════
# 4. API ENDPOINT TESTLERİ
# ══════════════════════════════════════════════════
class SensorDataReceiverTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('sensor-data')
        self.gecerli_veri = {
            "device_id":    "SENSOR_01",
            "temperature":  25.5,
            "humidity":     55.0,
            "soil_moisture": 40.0,
        }

    def test_gecerli_veri_201(self):
        response = self.client.post(self.url, self.gecerli_veri, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_gecerli_veri_karar_donuyor(self):
        response = self.client.post(self.url, self.gecerli_veri, format='json')
        self.assertIn("karar", response.data)

    def test_gecerli_veri_kayit_id_donuyor(self):
        response = self.client.post(self.url, self.gecerli_veri, format='json')
        self.assertIn("kayit_id", response.data)

    def test_eksik_alan_400(self):
        eksik = {"device_id": "SENSOR_02", "temperature": 25.0}
        response = self.client.post(self.url, eksik, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_aralik_disi_sicaklik_400(self):
        hatali = {**self.gecerli_veri, "temperature": 150.0}
        response = self.client.post(self.url, hatali, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_kuru_toprak_sulama_karari(self):
        kuru = {**self.gecerli_veri, "soil_moisture": 20.0}
        response = self.client.post(self.url, kuru, format='json')
        self.assertIn("Sulama sistemi başlatıldı", response.data["karar"])

    def test_doygun_toprak_durdurma_karari(self):
        doygun = {**self.gecerli_veri, "soil_moisture": 80.0}
        response = self.client.post(self.url, doygun, format='json')
        self.assertIn("Sulama durduruldu", response.data["karar"])


class IstatistikselAnalizTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('analiz')

    def test_veri_yokken_404(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_veri_varken_200(self):
        SensorData.objects.create(
            device_id="S1", temperature=25.0,
            humidity=50.0, soil_moisture=40.0
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_yanit_anahtarlari(self):
        SensorData.objects.create(
            device_id="S1", temperature=25.0,
            humidity=50.0, soil_moisture=40.0
        )
        response = self.client.get(self.url)
        self.assertIn("toprak_nemi_analizi", response.data)
        self.assertIn("sicaklik_analizi",    response.data)


# ══════════════════════════════════════════════════
# 5. VALIDATOR TESTLERİ (mevcut test_dogrulama.py
#    Django test framework'üne taşındı)
# ══════════════════════════════════════════════════
class SensorValidatorTest(TestCase):

    def test_gecerli_veri(self):
        s = sensor_verisini_dogrula({
            "device_id": "S1", "temperature": 25.0,
            "humidity": 55.0, "soil_moisture": 45.0
        })
        self.assertTrue(s["gecerli"])

    def test_eksik_alan(self):
        s = sensor_verisini_dogrula({"device_id": "S1", "temperature": 25.0})
        self.assertFalse(s["gecerli"])

    def test_aralik_disi_sicaklik(self):
        s = sensor_verisini_dogrula({
            "device_id": "S1", "temperature": 150.0,
            "humidity": 55.0, "soil_moisture": 45.0
        })
        self.assertFalse(s["gecerli"])

    def test_bos_device_id(self):
        s = sensor_verisini_dogrula({
            "device_id": "", "temperature": 25.0,
            "humidity": 55.0, "soil_moisture": 45.0
        })
        self.assertFalse(s["gecerli"])

    def test_dusuk_toprak_nemi_uyari(self):
        s = sensor_verisini_dogrula({
            "device_id": "S1", "temperature": 25.0,
            "humidity": 55.0, "soil_moisture": 10.0
        })
        self.assertTrue(s["gecerli"])
        self.assertTrue(len(s["uyarilar"]) > 0)


class HavaDurumuValidatorTest(TestCase):

    def test_gecerli_hava_durumu(self):
        s = hava_durumu_cevabini_dogrula({
            "city": "Malatya", "temperature": 22.0,
            "humidity": 60.0, "description": "Açık"
        })
        self.assertTrue(s["gecerli"])

    def test_eksik_sehir(self):
        s = hava_durumu_cevabini_dogrula({
            "temperature": 22.0, "humidity": 60.0, "description": "Açık"
        })
        self.assertFalse(s["gecerli"])


class HTTPDogrulamaTest(TestCase):

    def test_200_gecerli(self):
        self.assertTrue(genel_cevap_dogrula({}, 200)["gecerli"])

    def test_400_gecersiz(self):
        self.assertFalse(genel_cevap_dogrula({}, 400)["gecerli"])

    def test_500_gecersiz(self):
        self.assertFalse(genel_cevap_dogrula({}, 500)["gecerli"])

    def test_429_uyari(self):
        s = genel_cevap_dogrula({}, 429)
        self.assertTrue(s["gecerli"])
        self.assertTrue(len(s["uyarilar"]) > 0)


# ══════════════════════════════════════════════════
# 6. DASHBOARD VIEW TESTLERİ
# ══════════════════════════════════════════════════
from django.test import TestCase, Client
from django.urls import reverse

class DashboardViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        SensorData.objects.create(
            device_id="SENSOR_01",
            temperature=25.0,
            humidity=55.0,
            soil_moisture=40.0,
        )

    def test_dashboard_200(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_filtre_cihaz(self):
        response = self.client.get(reverse('dashboard'), {'cihaz': 'SENSOR_01'})
        self.assertEqual(response.status_code, 200)

    def test_sensor_listesi_200(self):
        response = self.client.get(reverse('sensor_listesi'))
        self.assertEqual(response.status_code, 200)

    def test_sensor_ekle_get_200(self):
        response = self.client.get(reverse('sensor_ekle'))
        self.assertEqual(response.status_code, 200)

    def test_sensor_ekle_gecerli_post(self):
        response = self.client.post(reverse('sensor_ekle'), {
            'device_id':    'SENSOR_02',
            'temperature':  22.0,
            'humidity':     50.0,
            'soil_moisture': 35.0,
        })
        self.assertEqual(SensorData.objects.filter(device_id='SENSOR_02').count(), 1)

    def test_sensor_ekle_gecersiz_post(self):
        response = self.client.post(reverse('sensor_ekle'), {
            'device_id':    '',
            'temperature':  22.0,
            'humidity':     50.0,
            'soil_moisture': 35.0,
        })
        # Hatalı veri → aynı sayfada kalır, yönlendirme olmaz
        self.assertEqual(response.status_code, 200)

    def test_sensor_sil_post(self):
        self.client.post(reverse('sensor_sil', args=['SENSOR_01']))
        self.assertEqual(SensorData.objects.filter(device_id='SENSOR_01').count(), 0)
