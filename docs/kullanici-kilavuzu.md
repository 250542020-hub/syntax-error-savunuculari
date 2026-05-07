# 📖 Kullanıcı Kılavuzu

Akıllı Tarım Yönetim Sistemi'ni kurmak, çalıştırmak ve kullanmak için adım adım rehber.

---

## 📋 İçindekiler

1. [Sistem Gereksinimleri](#sistem-gereksinimleri)
2. [Kurulum](#kurulum)
3. [Uygulamayı Başlatma](#uygulamayı-başlatma)
4. [Kullanım](#kullanım)
5. [Sorun Giderme](#sorun-giderme)

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
    source venv/bin/activate

### Adım 3 — Bağımlılıkları Yükle

    pip install -r requirements.txt

### Adım 4 — PostgreSQL Veritabanını Hazırla

PostgreSQL'e bağlanıp veritabanı ve kullanıcı oluşturun:

    CREATE DATABASE akilli_tarim_db;
    CREATE USER tarim_user WITH PASSWORD 'sifreniz';
    GRANT ALL PRIVILEGES ON DATABASE akilli_tarim_db TO tarim_user;

### Adım 5 — Veritabanı Tablolarını Oluştur

    python manage.py migrate

### Adım 6 — Yönetici Hesabı Oluştur

    python manage.py createsuperuser

Kullanıcı adı, e-posta ve şifre belirlemeniz istenecektir.

---

## 🚀 Uygulamayı Başlatma

İki ayrı terminal penceresi açın.

**Terminal 1 — Django Sunucusunu Başlat:**

    source venv/bin/activate
    python manage.py runserver

Sunucu http://localhost:8000 adresinde çalışmaya başlar.

**Terminal 2 — Sensör Simülatörünü Başlat:**

    source venv/bin/activate
    python simulator.py

Simülatör, gerçek bir tarladaki sensörleri taklit ederek otomatik veri üretir ve API'ye gönderir.

---

## 🖥️ Kullanım

### Yönetici Paneline Giriş

Tarayıcıda şu adresi açın:

    http://localhost:8000/admin/

Kurulum sırasında oluşturduğunuz bilgilerle giriş yapın. Panelde şunları yapabilirsiniz:

- Gelen sensör verilerini gerçek zamanlı izleyin
- Geçmiş ölçümleri filtreleyin ve sorgulayın
- Sistem tarafından üretilen sulama kararlarını görüntüleyin
- Kullanıcı hesaplarını yönetin

### Dashboard Kartları

| Kart | Açıklama |
|---|---|
| Toprak Nemi | Anlık toprak nem değeri (%) |
| Sıcaklık | Hava sıcaklığı (°C) |
| Hava Nemi | Bağıl nem oranı (%) |
| Sistem Kararı | Son üretilen sulama önerisi |

### Sensör Verilerini Görüntüleme

1. Sol menüden **Sensor Data** bölümüne tıklayın.
2. Tarih aralığına veya sensör kimliğine göre filtreleme yapın.
3. İlgili kaydın üzerine tıklayarak detay sayfasına ulaşın.

### Analiz Raporunu Görme

Tarayıcıda şu adresi açın:

    http://localhost:8000/api/analysis/

Son 100 ölçüme ait ortalama, medyan ve standart sapma değerleri JSON formatında görüntülenir.

---

## 🔧 Sorun Giderme

### Sunucu başlamıyor

1. Sanal ortamın aktif olduğunu kontrol edin — terminalin başında `(venv)` görünmelidir.
2. Bağımlılıkların eksiksiz yüklendiğini doğrulayın: `pip install -r requirements.txt`
3. Migrate adımının çalıştırıldığını kontrol edin: `python manage.py migrate`

---

### Veritabanına bağlanılamıyor

**Belirti:** `django.db.utils.OperationalError: could not connect to server`

1. PostgreSQL servisinin çalıştığını kontrol edin:

       brew services list | grep postgresql   # macOS
       sudo systemctl status postgresql       # Ubuntu

2. Veritabanı adı, kullanıcı adı ve şifrenin doğru olduğunu kontrol edin.
3. Gerekirse PostgreSQL'i yeniden başlatın:

       brew services restart postgresql   # macOS
       sudo systemctl restart postgresql  # Ubuntu

---

### Simülatör veri gönderemiyor

1. Django sunucusunun çalışır durumda olduğunu kontrol edin.
2. Simülatörü çalıştırırken sanal ortamın aktif olduğunu doğrulayın.
3. Tarayıcıdan http://localhost:8000/api/sensor-data/ adresine erişerek sunucu yanıtını test edin.

---

### pip install sırasında hata

1. Python sürümünü kontrol edin: `python3 --version` (3.10+ olmalı)
2. pip'i güncelleyin: `pip install --upgrade pip`
3. macOS'ta Xcode komut satırı araçlarının yüklü olduğunu kontrol edin:

       xcode-select --install

---

### Admin parolasını unuttum

    python manage.py changepassword <kullanici_adi>

---

## 📞 Destek

Sorun giderme adımları işe yaramazsa proje deposundaki Issues sekmesinden yeni bir konu açabilirsiniz:

    https://github.com/250542020-hub/syntax-error-savunuculari/issues
