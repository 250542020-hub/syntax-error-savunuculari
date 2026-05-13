# 📡 API Dokümantasyonu

Akıllı Tarım Yönetim Sistemi REST API referans belgesidir. Bu dokümanda tüm endpoint'ler, istek/yanıt formatları, kimlik doğrulama yöntemleri ve hata kodları açıklanmaktadır.

---

## 🔧 Genel Bilgiler

| Özellik | Değer |
|---|---|
| Temel URL | `http://localhost:8000` |
| API Versiyonu | v1 |
| Veri Formatı | JSON |
| Karakter Kodlaması | UTF-8 |
| Kimlik Doğrulama | Token / Session |

---

## 🔐 Kimlik Doğrulama

Tüm `/api/...` endpoint'leri kimlik doğrulama gerektirir (`IsAuthenticated`). İki yöntem desteklenir:

* **Token Authentication** → IoT cihazları ve simülatör için
* **Session Authentication** → Tarayıcı üzerinden giriş yapan kullanıcılar için

### Token Alma

    POST /api/token/

**İstek Gövdesi:**

    {
      "username": "kullanici_adi",
      "password": "sifreniz"
    }

**Başarılı Yanıt (200 OK):**

    {
      "token": "a1b2c3d4e5f6..."
    }

Bu token, sonraki tüm isteklerde aşağıdaki HTTP başlığı (header) ile gönderilmelidir:

    Authorization: Token a1b2c3d4e5f6...

> **Not:** Sensör cihazları için ayrı bir kullanıcı oluşturup token üretmesi önerilir (örn: `simulator_user`).

### Web Arayüzü Girişi

Tarayıcı üzerinden giriş için:

    GET  /giris/        # Giriş formu
    POST /giris/        # Form gönderimi
    POST /cikis/        # Çıkış

---

## 📮 API Endpoint Listesi

### 1. Sensör Verisi Gönderme

    POST /api/sensor-data/

IoT sensörlerinden gelen anlık çevresel verileri sisteme kaydeder. Veriler önce `validators.py` üzerinden doğrulanır. Toprak nemine göre otomatik sulama kararı üretilir.

**Gerekli Başlıklar (Headers):**

    Content-Type: application/json
    Authorization: Token <token_buraya>

**İstek Gövdesi (Request Body):**

    {
      "device_id": "SENSOR_01",
      "temperature": 28.5,
      "humidity": 65.2,
      "soil_moisture": 27.8
    }

| Alan | Tür | Zorunlu | Geçerli Aralık | Açıklama |
|---|---|---|---|---|
| `device_id` | string | ✅ | 1 – 50 karakter, boş olamaz | Sensörün benzersiz kimlik numarası |
| `temperature` | float | ✅ | -10.0 ile 60.0 (°C) | Hava sıcaklığı |
| `humidity` | float | ✅ | 0.0 ile 100.0 (%) | Bağıl hava nemi oranı |
| `soil_moisture` | float | ✅ | 0.0 ile 100.0 (%) | Toprak nem oranı |

**Başarılı Yanıt — Sulama Gerektiğinde (201 Created):**

Toprak nemi `< %30` olduğunda:

    {
      "mesaj": "Veri başarıyla işlendi",
      "karar": "KRİTİK: Toprak kuru! Sulama sistemi başlatıldı. ✅",
      "kayit_id": 142,
      "uyarilar": []
    }

**Başarılı Yanıt — Toprak Doygunken (201 Created):**

Toprak nemi `> %70` olduğunda:

    {
      "mesaj": "Veri başarıyla işlendi",
      "karar": "UYARI: Toprak doygun. Sulama durduruldu. 🛑",
      "kayit_id": 143,
      "uyarilar": []
    }

**Başarılı Yanıt — İdeal Durumda (201 Created):**

Toprak nemi `%30 - %70` arasında olduğunda:

    {
      "mesaj": "Veri başarıyla işlendi",
      "karar": "DURUM: Nem ideal. İşlem gerekmiyor. 🌾",
      "kayit_id": 144,
      "uyarilar": []
    }

**Doğrulama Uyarıları (`uyarilar` Alanı):**

İsteğin başarılı olduğu ancak ölçüm değerinin kritik olduğu durumlarda `uyarilar` dizisi dolu döner:

* Toprak nemi `< %15` → `"Toprak nemi kritik seviyede dusuk: 10.0%"`
* Sıcaklık `> 40°C` → `"Sicaklik asiri yuksek: 45.0 derece"`

---

### 2. İstatistiksel Analiz Raporu

    GET /api/analysis/

Veritabanındaki son **100** sensör ölçümüne ait TensorFlow tabanlı istatistiksel analizi JSON formatında döndürür.

**Gerekli Başlıklar:**

    Authorization: Token <token_buraya>

**Başarılı Yanıt (200 OK):**

    {
      "toprak_nemi_analizi": {
        "ortalama": 42.31,
        "medyan": 41.80,
        "standart_sapma": 5.24,
        "veri_adedi": 100
      },
      "sicaklik_analizi": {
        "ortalama": 26.74,
        "medyan": 26.50,
        "standart_sapma": 3.18,
        "veri_adedi": 100
      }
    }

**Veri Yetersiz (404 Not Found):**

    {
      "hata": "Analiz için yeterli veri yok."
    }

---

### 3. Token Alma

    POST /api/token/

Bkz. üstteki [Kimlik Doğrulama](#-kimlik-doğrulama) bölümü.

---

### 4. Yönetici Paneli

    GET /admin/

Django'nun yerleşik admin arayüzü. Tüm sensör verilerini, kullanıcı hesaplarını ve token'ları yönetmek için kullanılır. Tarayıcıdan erişilir; yalnızca `is_staff = True` olan kullanıcılar giriş yapabilir.

---

### 5. Web Arayüzü (Dashboard)

API olmasa da yönetim paneline ait sayfaların listesi:

| URL | Yöntem | Açıklama |
|---|---|---|
| `/` | GET | Ana dashboard — grafikler, son 50 ölçüm, filtreleme |
| `/sensorler/` | GET | Kayıtlı sensörlerin listesi |
| `/sensor-ekle/` | GET / POST | Manuel sensör verisi ekleme formu |
| `/sensor-sil/<device_id>/` | POST | Belirli bir sensörün tüm verilerini silme |
| `/giris/` | GET / POST | Kullanıcı girişi |
| `/cikis/` | POST | Çıkış |

Tüm dashboard sayfaları `@login_required` ile korunmaktadır.

---

## ⚠️ Hata Kodları

| Kod | Anlamı | Tipik Durum |
|---|---|---|
| `200` | OK | İstek başarıyla işlendi (GET) |
| `201` | Created | Yeni kayıt oluşturuldu (POST /api/sensor-data/) |
| `400` | Bad Request | Eksik veya hatalı istek gövdesi, doğrulama hatası |
| `401` | Unauthorized | Token eksik, geçersiz veya süresi dolmuş |
| `403` | Forbidden | Yetkisiz erişim girişimi |
| `404` | Not Found | Endpoint bulunamadı veya veri yok |
| `500` | Internal Server Error | Sunucu tarafında beklenmeyen hata |

**Hata Yanıtı Örneği — Doğrulama Hatası (400):**

    {
      "hata": "Geçersiz veri",
      "detaylar": [
        "Zorunlu alan eksik: 'soil_moisture'",
        "'temperature' degeri (150.0) gecerli aralik disinda [-10.0 - 60.0]"
      ]
    }

**Hata Yanıtı Örneği — Yetkisiz Erişim (401):**

    {
      "detail": "Authentication credentials were not provided."
    }

---

## 🧪 cURL Test Örnekleri

### 1. Token Alma

    curl -X POST http://localhost:8000/api/token/ \
      -H "Content-Type: application/json" \
      -d '{"username": "simulator_user", "password": "sifreniz"}'

### 2. Sensör Verisi Gönderme

    curl -X POST http://localhost:8000/api/sensor-data/ \
      -H "Content-Type: application/json" \
      -H "Authorization: Token a1b2c3d4e5f6..." \
      -d '{
        "device_id": "SENSOR_01",
        "temperature": 28.5,
        "humidity": 65.2,
        "soil_moisture": 27.8
      }'

### 3. Analiz Raporunu Çekme

    curl http://localhost:8000/api/analysis/ \
      -H "Authorization: Token a1b2c3d4e5f6..."

---

## 🔄 Veri Akışı

    IoT Sensör / Simülatör
            │
            │  1. POST /api/token/  (sadece ilk açılışta)
            ▼
        Token alır
            │
            │  2. POST /api/sensor-data/
            │     Header: Authorization: Token ...
            ▼
        Django API (api/views.py)
            │
            ├──► validators.py     (alan/aralık doğrulama)
            │
            ├──► PostgreSQL        (SensorData.objects.create)
            │
            └──► sulama_karari_uret(soil_moisture)
                     │
                     ▼
                JSON yanıt (201 Created)
                {mesaj, karar, kayit_id, uyarilar}

Analiz endpoint'i için akış:

    GET /api/analysis/
            │
            ▼
        Son 100 ölçüm çekilir
            │
            ▼
        TarimAnalizMotoru.analiz_et()
            │  → tf.constant → reduce_mean / sort / reduce_std
            ▼
        JSON yanıt (200 OK)

---

## 📌 Notlar

* Tüm tarih/saat değerleri sunucu tarafında otomatik atanır (`auto_now_add=True`). İstek gövdesinde gönderilmesi gerekmez.
* Ondalık değerler nokta (`.`) ile ayrılır.
* `device_id` alanına HTML/JS payload'ı enjekte edilemez; backend tarafında uzunluk ve tip kontrolü yapılır (`max 50 karakter`).
* `simulator.py` çalıştırıldığında bu endpoint'lere otomatik veri gönderir. Çalıştırmadan önce `SIMULATOR_TOKEN` veya `SIMULATOR_PASSWORD` ortam değişkeninin ayarlanması gerekir (detay için `docs/kullanici-kilavuzu.md`).

---

## 🔗 İlgili Dosyalar

| Dosya | Açıklama |
|---|---|
| `api/views.py` | Endpoint sınıfları (`SensorDataReceiver`, `IstatistikselAnaliz`) |
| `api/validators.py` | Sensör verisi ve hava durumu doğrulama fonksiyonları |
| `api/error_handler.py` | Standart hata/başarı yanıt üreticileri |
| `api/models.py` | `SensorData` veritabanı modeli |
| `tarim_projesi/urls.py` | URL yönlendirmeleri |
| `simulator.py` | Token destekli sensör simülatörü |
