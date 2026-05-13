# 📖 Kullanıcı Kılavuzu

Akıllı Tarım Yönetim Sistemi'ni kurmak, çalıştırmak ve kullanmak için adım adım rehber.

---

## 📋 İçindekiler

1. [Sistem Gereksinimleri](#-sistem-gereksinimleri)
2. [Kurulum](#-kurulum)
3. [Ortam Değişkenleri](#-ortam-değişkenleri)
4. [Uygulamayı Başlatma](#-uygulamayı-başlatma)
5. [Kullanım](#-kullanım)
6. [Sorun Giderme](#-sorun-giderme)

---

## 💻 Sistem Gereksinimleri

| Bileşen | Minimum |
|---|---|
| İşletim Sistemi | macOS 12+, Ubuntu 20.04+, Windows 10+ |
| Python | 3.10 veya üzeri |
| PostgreSQL | 13 veya üzeri |
| RAM | 4 GB |
| Disk | 2 GB boş alan |

---

## ⚙️ Kurulum

### Adım 1 — Repoyu İndir

    git clone https://github.com/250542020-hub/syntax-error-savunuculari.git
    cd syntax-error-savunuculari

### Adım 2 — Sanal Ortam Oluştur

    python3 -m venv venv
    source venv/bin/activate          # macOS / Linux
    venv\Scripts\activate             # Windows

### Adım 3 — Bağımlılıkları Yükle

    pip install --upgrade pip
    pip install -r requirements.txt

### Adım 4 — PostgreSQL Veritabanını Hazırla

PostgreSQL'e bağlanıp veritabanı ve kullanıcıyı oluşturun:

    psql -U postgres

    CREATE DATABASE akilli_tarim_db;
    CREATE USER tarim_user WITH PASSWORD 'guclu_bir_sifre';
    GRANT ALL PRIVILEGES ON DATABASE akilli_tarim_db TO tarim_user;
    \q

> **Önemli:** Burada belirlediğiniz `kullanıcı adı`, `şifre` ve `veritabanı adı` bilgilerini bir sonraki adımda ortam değişkeni olarak tanımlayacaksınız.

### Adım 5 — Ortam Değişkenlerini Ayarla

`settings.py` veritabanı bağlantı bilgilerini ortam değişkenlerinden okur. Detay için bir sonraki bölüme bakın.

### Adım 6 — Veritabanı Tablolarını Oluştur

    python manage.py migrate

Bu komut hem proje tablolarını hem de token kimlik doğrulaması için gereken `authtoken_token` tablosunu oluşturur.

### Adım 7 — Yönetici Hesabı Oluştur

Django admin paneli ve web dashboard'a giriş yapacak hesap:

    python manage.py createsuperuser

Kullanıcı adı, e-posta ve **en az 10 karakterlik** bir şifre belirlemeniz istenecektir (yaygın şifreler reddedilir).

### Adım 8 — Simülatör İçin Ayrı Kullanıcı (Opsiyonel ama Önerilen)

Simülatörü kendi token'ı ile çalıştırmak için ayrı bir hesap açın:

    python manage.py createsuperuser
    # Örnek: kullanıcı adı = simulator_user

---

## 🔐 Ortam Değişkenleri

Aşağıdaki ortam değişkenleri tanımlanmalıdır. Linux/macOS'ta `.env` dosyası veya `export` komutu kullanılabilir; Windows'ta `set` komutu kullanılır.

### Veritabanı Ayarları

| Değişken | Açıklama | Varsayılan |
|---|---|---|
| `DB_NAME` | Veritabanı adı | `akilli_tarim_db` |
| `DB_USER` | PostgreSQL kullanıcısı | `postgres` |
| `DB_PASSWORD` | Kullanıcı şifresi | _(boş)_ |
| `DB_HOST` | Veritabanı sunucusu | `127.0.0.1` |
| `DB_PORT` | Port | `5432` |

### Django Ayarları

| Değişken | Açıklama | Varsayılan |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django güvenlik anahtarı | _(geliştirme anahtarı)_ |
| `DJANGO_DEBUG` | `True` veya `False` | `True` |

### Simülatör Ayarları

| Değişken | Açıklama |
|---|---|
| `SIMULATOR_TOKEN` | Hazır token (varsa) |
| `SIMULATOR_USER` | Kullanıcı adı (varsayılan: `simulator_user`) |
| `SIMULATOR_PASSWORD` | Kullanıcı şifresi (token yoksa zorunlu) |

### Linux / macOS Örneği

    export DB_USER=tarim_user
    export DB_PASSWORD=guclu_bir_sifre
    export DJANGO_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")
    export SIMULATOR_USER=simulator_user
    export SIMULATOR_PASSWORD=simulator_sifresi

### Windows (PowerShell) Örneği

    $env:DB_USER = "tarim_user"
    $env:DB_PASSWORD = "guclu_bir_sifre"
    $env:SIMULATOR_USER = "simulator_user"
    $env:SIMULATOR_PASSWORD = "simulator_sifresi"

> **Üretim ortamı:** Production'a alırken `DJANGO_DEBUG=False` yapın. Bu, otomatik olarak HTTPS yönlendirmesi, güvenli cookie ve HSTS gibi koruma ayarlarını aktive eder (`settings.py` satır 146).

---

## 🚀 Uygulamayı Başlatma

İki ayrı terminal penceresi açın.

### Terminal 1 — Django Sunucusu

    source venv/bin/activate
    python manage.py runserver

Sunucu `http://localhost:8000` adresinde çalışmaya başlar.

### Terminal 2 — Sensör Simülatörü

    source venv/bin/activate
    export SIMULATOR_USER=simulator_user
    export SIMULATOR_PASSWORD=simulator_sifresi
    python simulator.py

Simülatör önce `/api/token/` üzerinden token alır, ardından her 5 saniyede bir rastgele sensör verisi üretip `/api/sensor-data/` endpoint'ine gönderir. Terminalde örnek çıktı:

    Token alindi: a1b2c3d4e5...
    Akilli Tarim Simulatoru Baslatildi (Yetkilendirilmis)...
    Gonderilen: {'device_id': 'SENSOR_01', 'temperature': 24.5, ...} | Cevap: DURUM: Nem ideal. İşlem gerekmiyor. 🌾

---

## 🖥️ Kullanım

### Giriş

Tarayıcıda:

    http://localhost:8000/giris/

Kurulum sırasında oluşturduğunuz yönetici bilgileriyle giriş yapın. Başarılı girişten sonra otomatik olarak ana dashboard'a yönlendirilirsiniz.

### Ana Dashboard (`/`)

| Bölüm | Açıklama |
|---|---|
| Özet Kartlar | Toplam kayıt sayısı, son sıcaklık, son toprak nemi, son hava nemi |
| Grafikler | Son 20 ölçümün sıcaklık ve nem zaman grafikleri (Chart.js) |
| Filtreleme | Başlangıç/bitiş tarihi ve cihaz ID'sine göre arama |
| Veri Tablosu | Son 50 sensör kaydı, otomatik sulama durumu badge'i |

Toprak nemi `< %30` olan satırlar ⚠️ simgesi ve kırmızı "Sulama Gerekli" rozeti ile işaretlenir.

### Sensör Listesi (`/sensorler/`)

* Kayıtlı tüm sensörleri görüntüleme
* Belirli bir sensörün tüm verilerini silme (onay penceresi ile)

### Manuel Veri Girişi (`/sensor-ekle/`)

Test amacıyla veya simülatör çalışmadığında elle veri eklemek için kullanılır. Girilen değerler `validators.py` üzerinden doğrulanır:

* `device_id` → 1–50 karakter, boş olamaz
* `temperature` → -10 ile 60 °C arası
* `humidity` → 0 ile 100 % arası
* `soil_moisture` → 0 ile 100 % arası

### Django Admin Paneli (`/admin/`)

Gelişmiş yönetim için Django'nun yerleşik admin arayüzü:

    http://localhost:8000/admin/

Sol menüden **Sensör Verileri** bölümüne tıklayarak ham veriyi görüntüleyebilir, tarih veya cihaz ID'sine göre filtreleyebilir, kullanıcıları ve token'ları yönetebilirsiniz.

### Analiz Raporu (`/api/analysis/`)

Token ile veya tarayıcıda giriş yaptıktan sonra:

    http://localhost:8000/api/analysis/

Son 100 ölçüme ait ortalama, medyan, standart sapma ve veri adedi JSON formatında döner. Detay için `docs/api-dokumantasyon.md` belgesine bakın.

### Çıkış

Sağ üstteki çıkış bağlantısına tıklayarak veya doğrudan:

    POST http://localhost:8000/cikis/

---

## 🔧 Sorun Giderme

### Sunucu Başlamıyor

1. Sanal ortamın aktif olduğunu kontrol edin — terminalin başında `(venv)` görünmelidir.
2. Bağımlılıkların eksiksiz yüklendiğini doğrulayın: `pip install -r requirements.txt`
3. Migrate adımının çalıştırıldığını kontrol edin: `python manage.py migrate`
4. Ortam değişkenlerinin set edilip edilmediğini test edin: `echo $DB_USER`

---

### Veritabanına Bağlanılamıyor

**Belirti:** `django.db.utils.OperationalError: could not connect to server`

1. PostgreSQL servisinin çalıştığını kontrol edin:

       brew services list | grep postgresql       # macOS
       sudo systemctl status postgresql           # Ubuntu

2. `DB_USER`, `DB_PASSWORD`, `DB_NAME` ortam değişkenlerinin doğru ayarlandığını doğrulayın.
3. Veritabanına manuel bağlantı testi yapın:

       psql -U $DB_USER -d $DB_NAME -h $DB_HOST

4. Gerekirse PostgreSQL'i yeniden başlatın:

       brew services restart postgresql           # macOS
       sudo systemctl restart postgresql          # Ubuntu

---

### Simülatör Token Alamıyor

**Belirti:** `Hata: SIMULATOR_TOKEN veya SIMULATOR_PASSWORD ortam degiskenini ayarla.`

1. `SIMULATOR_USER` ve `SIMULATOR_PASSWORD` değişkenlerini set ettiğinizden emin olun.
2. Bu kullanıcı adının Django'da gerçekten oluşturulmuş olduğunu kontrol edin (`createsuperuser` veya admin panelinden).
3. Django sunucusunun çalıştığını doğrulayın — token endpoint'i `http://127.0.0.1:8000/api/token/` üzerinden hizmet veriyor.

**Belirti:** `HATA: Token gecersiz veya suresi dolmus.`

1. Admin panelinden ilgili kullanıcının token'ını silip yeniden oluşturun, ya da:

       python manage.py drf_create_token simulator_user

---

### API 401 Unauthorized Hatası

Tüm `/api/...` endpoint'leri kimlik doğrulama gerektirir. cURL veya başka araçlarla istek atarken `Authorization: Token ...` başlığını eklemeyi unutmayın. Detaylı örnek için `docs/api-dokumantasyon.md` belgesine bakın.

---

### pip install Sırasında Hata

1. Python sürümünü kontrol edin: `python3 --version` (3.10+ olmalı)
2. pip'i güncelleyin: `pip install --upgrade pip`
3. macOS'ta Xcode komut satırı araçlarının yüklü olduğunu kontrol edin:

       xcode-select --install

4. Windows'ta `psycopg2-binary` kurulumunda Visual C++ Build Tools gerekebilir.

---

### Admin Parolasını Unuttum

    python manage.py changepassword <kullanici_adi>

Şifrenizin en az 10 karakter olması ve yaygın şifrelerden olmaması gerekir (`AUTH_PASSWORD_VALIDATORS` aktif).

---

### Dashboard'da Veri Görünmüyor

1. Simülatörün veya manuel veri girişinin en az bir kayıt oluşturduğunu kontrol edin.
2. Filtre alanlarını temizleyin (sağ üstteki "Temizle" butonu).
3. Django admin panelinden `Sensör Verileri` tablosunu kontrol edin — kayıt var mı?

---

## 📞 Destek

Sorun giderme adımları işe yaramazsa proje deposundaki Issues sekmesinden yeni bir konu açabilirsiniz:

    https://github.com/250542020-hub/syntax-error-savunuculari/issues

İlgili belgeler:

* `docs/api-dokumantasyon.md` — Tüm endpoint'lerin detaylı dokümantasyonu
* `docs/ui_ux_tasarim_raporu.md` — Arayüz tasarım kararları
* `guvenlik_acigi_raporu.md` — Güvenlik denetimi raporu
* `hata_raporu.md` — Tespit edilen hatalar ve çözümleri
