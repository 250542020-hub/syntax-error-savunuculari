# 🌱 Akıllı Tarım Projesi — IoT Sensör Veri Toplama Modülü
## Gereksinim Analiz Raporu

> **Proje:** syntax-error-savunuculari  
> **Framework:** Django REST + PostgreSQL + MQTT  
> **Tarih:** Mayıs 2026

---

## 1. Sensörler ve Toplanan Veriler

Sistemde üç sensör parametresi aktif olarak kullanılmaktadır.

### 1.1 Sıcaklık — `temperature`

| Özellik | Değer |
|---|---|
| Model Alanı | `temperature = models.FloatField(verbose_name="Sıcaklık (°C)")` |
| Geçerli Aralık | `-10.0 °C` ÷ `60.0 °C` |
| Uyarı Eşiği | `> 40.0 °C` → *"Sıcaklık aşırı yüksek"* |
| Veri Tipi | `float` (tam sayı da kabul edilir) |
| Önerilen Donanım | DHT22 / SHT31 / DS18B20 (±0.5 °C hassasiyet) |

### 1.2 Hava Nemi — `humidity`

| Özellik | Değer |
|---|---|
| Model Alanı | `humidity = models.FloatField(verbose_name="Hava Nemi (%)")` |
| Geçerli Aralık | `0.0 %` ÷ `100.0 %` |
| Uyarı Eşiği | Henüz tanımlanmamış — `< 30 %` kuru, `> 85 %` yoğun önerilir |
| Veri Tipi | `float` |
| Önerilen Donanım | DHT22 / SHT31 (±2 % RH hassasiyet) |

> ⚠️ `humidity` `sensor_collector.log` içinde hiç görünmüyor. Collector'ın bu veriyi gönderip göndermediği doğrulanmalıdır.

### 1.3 Toprak Nemi — `soil_moisture`

| Özellik | Değer |
|---|---|
| Model Alanı | `soil_moisture = models.FloatField(verbose_name="Toprak Nemi (%)")` |
| Geçerli Aralık | `0.0 %` ÷ `100.0 %` |
| Kritik Eşik (düşük) | `< 15.0 %` → *"Toprak nemi kritik seviyede düşük"* |
| Sulama Kararı | `< 30 %` Sulama BAŞLAT · `30–70 %` İdeal · `> 70 %` Sulama DURDUR |
| Önerilen Donanım | Capacitive Soil Moisture v1.2 / TEROS-12 |

### 1.4 Gelecek Dönem — Önerilen Ek Sensörler

| Sensör | Ölçüm | Birim | Öncelik |
|---|---|---|---|
| Işık | Fotosentetik Aktif Radyasyon | µmol/m²/s | 🔴 Yüksek |
| pH | Toprak pH değeri | 0–14 | 🔴 Yüksek |
| Yağmur | Yağış miktarı | mm/saat | 🟡 Orta |
| CO2 | Karbondioksit | ppm | 🟡 Orta |
| Rüzgar | Hız | m/s | 🟢 Düşük |

---

## 2. Veri Toplama Sıklığı

Mevcut kodda veri toplama sıklığı tanımlanmamıştır. Üretilen `collector_config.json` dosyası bu eksiği kapatmaktadır.

| Senaryo | Sıcaklık | Hava Nemi | Toprak Nemi | Tetikleyici |
|---|---|---|---|---|
| Normal izleme | 15 dk | 15 dk | 10 dk | Zamanlayıcı |
| Kritik eşik aşımı | 1 dk | 1 dk | 1 dk | Otomatik — validators eşiği |
| Sulama aktifken | 5 dk | 5 dk | 2 dk | `sulama_karari_uret()` kararı |
| İstatistiksel analiz | Saatlik ort. | Saatlik ort. | Saatlik ort. | `IstatistikselAnaliz` API — `TarimAnalizMotoru` |

**Teknik notlar:**

- `auto_now_add=True` saniye hassasiyetindedir; yüksek frekanslı senaryo için milisaniye değerlendirilmelidir.
- `IstatistikselAnaliz` endpoint'indeki `queryset[:100]` sabit limiti zaman bazlı analize izin vermemektedir. `?start_date=&end_date=` parametresi eklenmelidir.
- `TarimAnalizMotoru` ortalama, medyan, standart sapma ve veri adedi döndürmektedir; bu istatistikler saatlik agregasyon için doğrudan kullanılabilir.

---

## 3. Veri Formatları

### 3.1 Collector → API — `POST /api/sensor/`

```json
{
  "device_id":     "SENSOR_01",
  "temperature":   25.4,
  "humidity":      62.3,
  "soil_moisture": 38.7
}
```

> ⚠️ **Alan Adı Uyumsuzluğu:** Collector şu an `sensor_id`, `sicaklik`, `toprak_nemi` göndermektedir. API `device_id`, `temperature`, `soil_moisture` beklemektedir. Üretilen `sensor_collector.py` bu sorunu çözmektedir.

### 3.2 Alan Kısıtlamaları

| Alan | Tip | Min | Max | Zorunlu |
|---|---|---|---|---|
| `device_id` | `string` | — | 50 karakter | ✅ |
| `temperature` | `float` | -10.0 | 60.0 | ✅ |
| `humidity` | `float` | 0.0 | 100.0 | ✅ |
| `soil_moisture` | `float` | 0.0 | 100.0 | ✅ |
| `timestamp` | `datetime` | — | — | ⚙️ Otomatik |

### 3.3 API Yanıt Formatları

**Başarılı (HTTP 201):**
```json
{
  "mesaj":    "Veri başarıyla işlendi",
  "karar":    "KRİTİK: Toprak kuru! Sulama sistemi başlatıldı. ✅",
  "kayit_id": 42,
  "uyarilar": ["Sıcaklık aşırı yüksek: 41 derece"]
}
```

**Hata (HTTP 400):**
```json
{
  "hata":     "Geçersiz veri",
  "detaylar": ["'soil_moisture' değeri (120.0) geçerli aralık dışında [0.0 - 100.0]"]
}
```

### 3.4 `TarimAnalizMotoru` Çıktı Formatı

`IstatistikselAnaliz` endpoint'i her parametre için şu yapıyı döndürür:

```json
{
  "toprak_nemi_analizi": {
    "ortalama":       38.7,
    "medyan":         37.2,
    "standart_sapma": 5.1,
    "veri_adedi":     100
  },
  "sicaklik_analizi": {
    "ortalama":       24.3,
    "medyan":         24.0,
    "standart_sapma": 2.8,
    "veri_adedi":     100
  }
}
```

---

## 4. Veri Güvenliği Gereksinimleri

### 4.1 Kimlik Doğrulama

`SensorDataReceiver` ve `IstatistikselAnaliz` endpoint'leri şu an kimlik doğrulaması olmadan erişilebilir durumdadır.

| Katman | Yöntem | Öncelik |
|---|---|---|
| API | `X-API-Key` header — `device_id` bazlı token | 🔴 Acil |
| Transport | HTTPS / TLS (Let's Encrypt) | 🔴 Acil |
| MQTT Broker | Kullanıcı adı + şifre veya TLS sertifikası | 🔴 Acil |
| Rate Limiting | DRF Throttle — sensör başına 10 istek/dk | 🟡 Orta |
| Cihaz Kaydı | Device whitelist — kayıtsız cihaz engellensin | 🟡 Orta |

### 4.2 Mevcut Doğrulama Katmanı

`validators.py` aşağıdaki kontrolleri sağlamaktadır:

| Kontrol | Durum |
|---|---|
| Zorunlu alan eksikliği | ✅ Uygulanmış |
| Sayısal tip doğrulaması | ✅ Uygulanmış |
| Aralık dışı değer reddi | ✅ Uygulanmış |
| İki seviyeli geri bildirim (`hatalar` / `uyarilar`) | ✅ Uygulanmış |
| Tüm kararların loglanması | ✅ Uygulanmış |
| Humidity kritik eşiği | ⚠️ Eksik — eklenmeli |

### 4.3 Loglama

| Seviye | Kapsam | Durum |
|---|---|---|
| `INFO` | Geçerli veri alındı | ✅ Mevcut |
| `WARNING` | Alan eksik, eşik aşımı | ✅ Mevcut |
| `ERROR` | Geçersiz veri, DB yazma hatası | ✅ Mevcut |
| `CRITICAL` | Güvenlik ihlalleri | ⚠️ Eksik |
| `AUDIT` | `sensor_sil` işlemleri | ⚠️ Eksik |

### 4.4 Veri Saklama

- `device_id` + konum ilişkisi kurulursa KVKK kapsamına girer
- **Retention policy:** Ham veri 1 yıl · Agregat veri 5 yıl
- PostgreSQL bağlantısı SSL zorunlu yapılandırılmalıdır
- MQTT payload şifreleme için TLS zorunludur
