# 📡 API Dokümantasyonu

Akıllı Tarım Yönetim Sistemi REST API referans belgesidir. Bu dokümanda tüm endpoint'ler, istek/yanıt formatları ve hata kodları açıklanmaktadır.

---

## 🔧 Genel Bilgiler

| Özellik | Değer |
|---|---|
| Temel URL | `http://localhost:8000` |
| API Versiyonu | v1 |
| Veri Formatı | JSON |
| Kimlik Doğrulama | Session / Token |

---

## 🔐 Kimlik Doğrulama

Yönetici paneline erişim için önce giriş yapılmalıdır.

    POST /admin/login/

Sensör cihazları için herhangi bir token gerekmez; cihaz kimliği istek gövdesinde iletilir.

---

## 📮 Endpoint Listesi

### 1. Sensör Verisi Gönderme

    POST /api/sensor-data/

IoT sensörlerinden gelen anlık çevresel verileri sisteme kaydeder. Gelen toprak nemi değeri %30'un altındaysa sistem otomatik olarak sulama komutu üretir.

**İstek Gövdesi (Request Body):**

    {
      "sensor_id": "sensor_01",
      "sicaklik": 28.5,
      "hava_nemi": 65.2,
      "toprak_nemi": 27.8
    }

| Alan | Tür | Zorunlu | Açıklama |
|---|---|---|---|
| `sensor_id` | string | ✅ | Sensörün benzersiz kimlik numarası |
| `sicaklik` | float | ✅ | Hava sıcaklığı (°C) |
| `hava_nemi` | float | ✅ | Bağıl nem oranı (%) |
| `toprak_nemi` | float | ✅ | Toprak nem oranı (%) |

**Başarılı Yanıt — sulama gerektiğinde (200 OK):**

    {
      "durum": "kaydedildi",
      "karar": "SULAMA SİSTEMİ BAŞLATILDI",
      "zaman_damgasi": "2025-05-07T14:32:11Z"
    }

**Başarılı Yanıt — sulama gerekmediğinde (200 OK):**

    {
      "durum": "kaydedildi",
      "karar": "Normal - Sulama Gerekmiyor",
      "zaman_damgasi": "2025-05-07T14:32:11Z"
    }

---

### 2. İstatistiksel Analiz Raporu

    GET /api/analysis/

Veritabanındaki son 100 sensör ölçümüne ait TensorFlow tabanlı istatistiksel analizi JSON formatında döndürür.

**Örnek Yanıt (200 OK):**

    {
      "toprak_nemi": {
        "ortalama": 42.3,
        "medyan": 41.8,
        "standart_sapma": 5.2
      },
      "sicaklik": {
        "ortalama": 26.7,
        "medyan": 26.5,
        "standart_sapma": 3.1
      },
      "veri_sayisi": 100
    }

---

### 3. Yönetici Paneli

    GET /admin/

Tüm geçmiş sensör verilerini, sistem kararlarını ve kullanıcı yönetimini sunan Django admin arayüzüdür. Tarayıcı üzerinden erişilir; yalnızca yetkili yöneticiler giriş yapabilir.

---

## ⚠️ Hata Kodları

| Kod | Anlamı | Açıklama |
|---|---|---|
| `200` | OK | İstek başarıyla işlendi |
| `400` | Bad Request | Eksik veya hatalı istek gövdesi |
| `401` | Unauthorized | Kimlik doğrulama başarısız |
| `404` | Not Found | İstenilen kaynak bulunamadı |
| `500` | Internal Server Error | Sunucu tarafında beklenmeyen hata |

**Hata Yanıtı Örneği (400):**

    {
      "hata": "Geçersiz istek",
      "detay": "toprak_nemi alanı zorunludur"
    }

---

## 🧪 Test Örneği (cURL)

Sensör verisi göndermek için:

    curl -X POST http://localhost:8000/api/sensor-data/ \
      -H "Content-Type: application/json" \
      -d '{"sensor_id": "sensor_01", "sicaklik": 28.5, "hava_nemi": 65.2, "toprak_nemi": 27.8}'

Analiz raporunu çekmek için:

    curl http://localhost:8000/api/analysis/

---

## 🔄 Veri Akışı

    IoT Sensör
        │
        │  POST /api/sensor-data/
        ▼
    Django API
        │
        ├──► PostgreSQL  (veri kaydedilir)
        │
        └──► TensorFlow  (nem < %30 ise sulama kararı üretilir)
                  │
                  ▼
             Yanıt JSON

---

## 📌 Notlar

- Tüm tarih/saat değerleri UTC formatındadır (ISO 8601).
- Ondalık değerler nokta (.) ile ayrılır.
- `simulator.py` çalıştırıldığında bu endpoint'e otomatik veri gönderilir; elle test gerekmez.
