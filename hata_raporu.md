# Veritabanı Bağlantı Hataları — Tespit ve Çözüm Raporu

**Proje:** Akıllı Tarım Yönetim Sistemi  
**Ekip:** Syntax Error Savunucuları  
**İncelenen Dosya:** `tarim_projesi/settings.py`  
**Tarih:** 05.05.2026

---

## Tespit Edilen Hatalar

### Hata 1 — Veritabanı SQLite, olması gereken PostgreSQL

**Sorun:** `settings.py` içinde `sqlite3` kullanılıyor. Proje dokümantasyonunda PostgreSQL seçilmiş, `requirements.txt` içinde `psycopg2-binary` kurulu ama bağlantı hâlâ SQLite'a yapılıyor.

**Hatalı kod:**
```python
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
```

**Düzeltme:**
```python
'ENGINE': 'django.db.backends.postgresql',
'NAME': os.environ.get('DB_NAME', 'akilli_tarim_db'),
```

---

### Hata 2 — Bağlantı Havuzu Tanımlanmamış

**Sorun:** `CONN_MAX_AGE` parametresi yazılmamış. Django'nun varsayılanı `0` olduğu için her HTTP isteğinde PostgreSQL'e yeni bağlantı açılıp kapanır. Birden fazla sensör veya eş zamanlı isteklerde bağlantı tükenmesi yaşanır.

**Düzeltme:**
```python
'CONN_MAX_AGE': 60,
'CONN_HEALTH_CHECKS': True,
'OPTIONS': {
    'connect_timeout': 5,
    'keepalives': 1,
    'keepalives_idle': 30,
    'keepalives_interval': 5,
    'keepalives_count': 5,
}
```

---

### Hata 3 — SECRET_KEY Açıkta

**Sorun:** Gizli anahtar doğrudan koda yazılmış ve Git'e yüklenmiş durumda. Güvenlik açığı oluşturur.

**Hatalı kod:**
```python
SECRET_KEY = 'django-insecure-akilli-tarim-gizli-anahtar'
```

**Düzeltme:**
```python
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-akilli-tarim-gizli-anahtar')
```

---

### Hata 4 — MIDDLEWARE'de Bozuk Satır

**Sorun:** `SecurityMiddleware` satırı markdown linki olarak yazılmış. Python bunu tanımaz, uygulama başlarken çöker.

**Hatalı kod:**
```python
'[django.middleware.security](http://django.middleware.security).SecurityMiddleware',
```

**Düzeltme:**
```python
'django.middleware.security.SecurityMiddleware',
```

---

### Hata 5 — CORS Tüm Kaynaklara Açık

**Sorun:** `CORS_ALLOW_ALL_ORIGINS = True` ayarı her adresten gelen isteği kabul eder. Güvenlik açığı oluşturur.

**Düzeltme:**
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
```

---

### Hata 6 — ALLOWED_HOSTS Boş

**Sorun:** `ALLOWED_HOSTS = []` bırakılmış. Production ortamında Django tüm istekleri reddeder.

**Düzeltme:**
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

---

### Hata 7 — api.loglama_config Import Hatası

**Sorun:** `settings.py` yüklenirken `api` modülü henüz tanınmıyor. `ModuleNotFoundError: No module named 'api'` hatası fırlatılıyor.

**Hatalı kod:**
```python
from api.loglama_config import LOGLAMA_AYARLARI
LOGGING = LOGLAMA_AYARLARI
```

**Düzeltme:**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

---

### Hata 8 — SQL Dosyasında FOREIGN KEY Eksik

**Sorun:** `toprak_nemi_olcumleri` tablosunda `sensor_id` sütununa FOREIGN KEY tanımlanmamış. Var olmayan bir sensör ID'siyle kayıt eklenebilir, veri bütünlüğü bozulur.

**Hatalı kod:**
```sql
sensor_id INTEGER NOT NULL,
```

**Düzeltme:**
```sql
sensor_id INTEGER NOT NULL REFERENCES sensorler(id) ON DELETE CASCADE,
```

---

## Özet Tablo

| # | Hata | Dosya | Önem | Durum |
|---|------|-------|------|-------|
| 1 | SQLite kullanılıyor, PostgreSQL olmalı | settings.py | 🔴 Kritik | Düzeltildi |
| 2 | Bağlantı havuzu tanımlanmamış | settings.py | 🔴 Kritik | Düzeltildi |
| 3 | SECRET_KEY hardcode | settings.py | 🔴 Kritik | Düzeltildi |
| 4 | MIDDLEWARE'de bozuk satır | settings.py | 🔴 Kritik | Düzeltildi |
| 5 | CORS herkese açık | settings.py | 🟠 Yüksek | Düzeltildi |
| 6 | ALLOWED_HOSTS boş | settings.py | 🟠 Yüksek | Düzeltildi |
| 7 | api.loglama_config import hatası | settings.py | 🔴 Kritik | Düzeltildi |
| 8 | FOREIGN KEY eksik | akilli_tarim_db.sql | 🔴 Kritik | Düzeltildi |
