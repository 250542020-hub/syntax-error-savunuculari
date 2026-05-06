"""
Akilli Tarim Yonetim Sistemi - Guvenlik Aciklari Tarama Testleri
================================================================
Calistirma:
    python manage.py test api.test_guvenlik

Bu test paketi su saldirilari simule eder:
  - XSS (Cross-Site Scripting)
  - SQL Injection
  - Yetkilendirme bypass denemeleri
  - CSRF kontrolu
  - Information disclosure (hata mesaji sizdirma)

Konum:  api/test_guvenlik.py  olarak kaydet.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from api.models import SensorData


class XSSTestleri(TestCase):
    """
    XSS (Cross-Site Scripting) acigi testleri.
    Saldirgan, kullanici verisine HTML/JS enjekte edip
    tarayicida calistirmaya calisir.
    """

    def setUp(self):
        self.client = Client()
        # Test icin yetkili bir kullanici olusturalim
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

    def test_01_dashboard_device_id_xss(self):
        """device_id alanina XSS payload enjekte et, dashboard'da escape ediliyor mu?"""
        xss_payload = "<script>alert('XSS')</script>"
        SensorData.objects.create(
            device_id=xss_payload,
            temperature=25.0, humidity=55.0, soil_moisture=45.0
        )
        response = self.client.get('/')
        icerik = response.content.decode('utf-8')

        # Eger payload ham haliyle (escape edilmeden) sayfada yer aliyorsa XSS var demektir
        if xss_payload in icerik:
            self.fail(
                "XSS ACIGI BULUNDU: device_id ham olarak HTML'e basildi.\n"
                "Olasi sebep: dashboard.html icindeki {{ grafik_verisi|safe }} filtresi.\n"
                "Cozum: |safe kaldirilmali, json_script kullanilmali."
            )
        # Escape edilmis hali olmali
        self.assertIn("&lt;script&gt;", icerik,
                      "device_id HTML escape edilmemis - olasi XSS")

    def test_02_dashboard_filtre_parametresi_xss(self):
        """URL filtre parametresine XSS payload"""
        payload = "<img src=x onerror=alert('XSS')>"
        response = self.client.get('/', {'cihaz': payload})
        icerik = response.content.decode('utf-8')
        self.assertNotIn(payload, icerik,
                         "Filtre parametresi escape edilmemis - reflected XSS riski")

    def test_03_javascript_context_xss(self):
        """JavaScript bloguna sizan XSS testi (en kritik)"""
        # </script> ile script tag'inden cikip yeni bir script aciyor
        payload = "</script><script>alert(1)</script>"
        SensorData.objects.create(
            device_id=payload,
            temperature=20.0, humidity=50.0, soil_moisture=40.0
        )
        response = self.client.get('/')
        icerik = response.content.decode('utf-8')
        # JS context'inden cikis basariliysa kritik XSS
        self.assertNotIn("</script><script>alert(1)</script>", icerik,
                         "KRITIK: JS context'inden cikis mumkun, |safe filtresi kaldirilmali")


class SQLInjectionTestleri(TestCase):
    """
    SQL Injection testleri.
    Django ORM parametreli sorgu kullanir,
    teorik olarak korumali ama yine de test edelim.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')
        SensorData.objects.create(device_id='SENSOR_01', temperature=25, humidity=55, soil_moisture=45)
        SensorData.objects.create(device_id='SENSOR_02', temperature=26, humidity=58, soil_moisture=42)

    def test_01_filtre_sql_injection_klasik(self):
        """Filtre parametresine klasik SQL injection payload'i"""
        payload = "'; DROP TABLE api_sensordata; --"
        response = self.client.get('/', {'cihaz': payload})

        # Tablo hala var mi kontrol et
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SensorData.objects.count(), 2,
                         "SQL Injection ile tablo silindi - ORM korumasi ASILDI")

    def test_02_filtre_sql_injection_or_bypass(self):
        """OR 1=1 tipi bypass denemesi"""
        payload = "' OR '1'='1"
        response = self.client.get('/', {'cihaz': payload})
        self.assertEqual(response.status_code, 200)
        # Bu payload icin 0 sonuc dönmeli (escape edildigi icin literal aranir)

    def test_03_tarih_filtresi_sql_injection(self):
        """Tarih filtresine injection - view crash etmemeli"""
        payload = "2025-01-01' OR 1=1 --"
        response = self.client.get('/', {'baslangic': payload})
        # Onemli: 500 (sunucu cokmesi) DONMEMELI.
        # Django ORM gecersiz tarihi yakalar, view zarif sekilde ele almali.
        self.assertNotEqual(response.status_code, 500,
                            "View bozuk tarih girdisinde cokuyor - try/except eksik")
        self.assertIn(response.status_code, [200, 400])

    def test_04_api_post_sql_injection(self):
        """API POST endpointine SQL injection"""
        api_client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        kotu_data = {
            "device_id": "SENSOR_X'; DROP TABLE api_sensordata; --",
            "temperature": 25.0, "humidity": 50.0, "soil_moisture": 40.0
        }
        response = api_client.post('/api/sensor-data/', kotu_data, format='json')
        self.assertEqual(SensorData.objects.count(), 3,
                         "API uzerinden SQL Injection basarili - veriler kayboldu")


class YetkilendirmeTestleri(TestCase):
    """
    API endpointlere kimlik dogrulama olmadan erisim denemeleri.
    """

    def test_01_api_anonim_get(self):
        """Anonim kullanici /api/analysis/ goruyor mu?"""
        response = APIClient().get('/api/analysis/')
        self.assertEqual(response.status_code, 401,
                         f"GUVENLIK: Anonim kullanici analiz API'sine erisebiliyor (kod: {response.status_code})")

    def test_02_api_anonim_post(self):
        """Anonim kullanici /api/sensor-data/ POST yapabiliyor mu?"""
        veri = {"device_id": "X", "temperature": 1, "humidity": 1, "soil_moisture": 1}
        response = APIClient().post('/api/sensor-data/', veri, format='json')
        self.assertEqual(response.status_code, 401,
                         f"GUVENLIK: Anonim kullanici veri yukleyebiliyor (kod: {response.status_code})")

    def test_03_dashboard_anonim_erisim(self):
        """Anonim kullanici dashboard'a erisebiliyor mu? (Olmamali)"""
        response = Client().get('/')
        self.assertNotEqual(response.status_code, 200,
                            "GUVENLIK: Dashboard auth olmadan erisilebilir durumda")

    def test_04_sensor_silme_anonim(self):
        """Anonim kullanici sensor silebiliyor mu?"""
        SensorData.objects.create(device_id='SILINMEZ_01', temperature=20, humidity=50, soil_moisture=40)
        Client().post('/sensor-sil/SILINMEZ_01/')
        self.assertTrue(
            SensorData.objects.filter(device_id='SILINMEZ_01').exists(),
            "GUVENLIK: Anonim kullanici sensor silebildi"
        )


class CSRFTestleri(TestCase):
    """CSRF koruma testleri (form bazli view'lar icin)."""

    def setUp(self):
        self.user = User.objects.create_user(username='csrfuser', password='testpass123')

    def test_01_csrf_olmadan_post(self):
        """CSRF token olmadan POST atilabiliyor mu?"""
        client = Client(enforce_csrf_checks=True)
        client.login(username='csrfuser', password='testpass123')
        response = client.post('/sensor-ekle/', {
            'device_id': 'CSRF_TEST', 'temperature': 25, 'humidity': 50, 'soil_moisture': 40
        })
        self.assertEqual(response.status_code, 403,
                         "GUVENLIK: CSRF korumasi devre disi - kod: %d" % response.status_code)


class HataMesajiSizdirmaTestleri(TestCase):
    """Information disclosure: stack trace, path, debug bilgisi sizmasin"""

    def setUp(self):
        self.user = User.objects.create_user(username='infouser', password='testpass123')
        self.api_client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_01_bozuk_veri_hata_mesaji(self):
        """Bozuk veri gonderildiginde Django stack trace'i sizmasin"""
        response = self.api_client.post('/api/sensor-data/', {
            "device_id": "X", "temperature": "BOZUK", "humidity": 50, "soil_moisture": 40
        }, format='json')
        if response.status_code == 400:
            cevap = response.json()
            hata_metni = str(cevap.get('hata', ''))
            yasak_kelimeler = ['Traceback', 'File "', '.py', 'django.', 'psycopg2']
            for kelime in yasak_kelimeler:
                self.assertNotIn(kelime, hata_metni,
                                 f"Information disclosure: '{kelime}' hata mesajinda goruluyor")