# 🗄️ PostgreSQL Veritabanı Tasarımı

## 📌 Amaç
Bu veritabanı, Akıllı Tarım Yönetim Sistemi için sensör verilerini, kullanıcı bilgilerini ve analiz sonuçlarını saklamak amacıyla tasarlanmıştır. Sistem, büyük veri ile çalışabileceği için performans ve ölçeklenebilirlik göz önünde bulundurulmuştur.

---

## 🧩 Tablolar

### 👤 users
- id (PRIMARY KEY)
- username (VARCHAR)
- email (VARCHAR)
- password (VARCHAR)
- created_at (TIMESTAMP)

### 🌾 fields
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- field_name (VARCHAR)
- location (VARCHAR)

### 📡 sensors
- id (PRIMARY KEY)
- field_id (FOREIGN KEY)
- sensor_type (VARCHAR)

### 📊 sensor_data
- id (PRIMARY KEY)
- sensor_id (FOREIGN KEY)
- temperature (FLOAT)
- humidity (FLOAT)
- soil_moisture (FLOAT)
- created_at (TIMESTAMP)

### 🤖 analysis
- id (PRIMARY KEY)
- sensor_data_id (FOREIGN KEY)
- prediction (TEXT)
- recommendation (TEXT)
- created_at (TIMESTAMP)

---

## 🔗 İlişkiler

- Bir kullanıcı birden fazla tarlaya sahip olabilir  
- Bir tarla birden fazla sensör içerir  
- Bir sensör sürekli veri üretir  
- Her veri için analiz sonucu oluşturulabilir  

İlişki zinciri:

User → Field → Sensor → SensorData → Analysis

---

## 🧾 SQL Tablo Oluşturma Kodları

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100),
    password VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fields (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    field_name VARCHAR(100),
    location VARCHAR(100)
);

CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    field_id INT REFERENCES fields(id),
    sensor_type VARCHAR(50)
);

CREATE TABLE sensor_data (
    id SERIAL PRIMARY KEY,
    sensor_id INT REFERENCES sensors(id),
    temperature FLOAT,
    humidity FLOAT,
    soil_moisture FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE analysis (
    id SERIAL PRIMARY KEY,
    sensor_data_id INT REFERENCES sensor_data(id),
    prediction TEXT,
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sensor_data_sensor_id ON sensor_data(sensor_id);
CREATE INDEX idx_sensor_data_time ON sensor_data(created_at);
CREATE INDEX idx_analysis_data ON analysis(sensor_data_id);


# 🗄️ Veritabanı Şema Tasarımı

## 📌 Amaç
Akıllı Tarım Yönetim Sistemi için kullanıcı bilgileri, sensör verileri ve yapay zeka analiz sonuçlarını saklayacak PostgreSQL veritabanı tasarlanmıştır.

---

## 🧩 Tablolar ve Sütunlar

### 👤 Users (Kullanıcılar)

| Sütun | Veri Tipi | Açıklama |
|---------|---------|---------|
| id | SERIAL | Birincil anahtar |
| username | VARCHAR(50) | Kullanıcı adı |
| email | VARCHAR(100) | E-posta |
| password | VARCHAR(255) | Şifre |
| created_at | TIMESTAMP | Oluşturulma tarihi |

---

### 🌾 Fields (Tarlalar)

| Sütun | Veri Tipi | Açıklama |
|---------|---------|---------|
| id | SERIAL | Birincil anahtar |
| user_id | INTEGER | Kullanıcı ID |
| field_name | VARCHAR(100) | Tarla adı |
| location | VARCHAR(200) | Konum |

---

### 📡 Sensors (Sensörler)

| Sütun | Veri Tipi | Açıklama |
|---------|---------|---------|
| id | SERIAL | Birincil anahtar |
| field_id | INTEGER | Tarla ID |
| sensor_type | VARCHAR(50) | Sensör tipi |

---

### 📊 Sensor_Data (Sensör Verileri)

| Sütun | Veri Tipi | Açıklama |
|---------|---------|---------|
| id | SERIAL | Birincil anahtar |
| sensor_id | INTEGER | Sensör ID |
| temperature | FLOAT | Sıcaklık |
| humidity | FLOAT | Nem |
| soil_moisture | FLOAT | Toprak nemi |
| created_at | TIMESTAMP | Veri zamanı |

---

### 🤖 Analysis (Analiz Sonuçları)

| Sütun | Veri Tipi | Açıklama |
|---------|---------|---------|
| id | SERIAL | Birincil anahtar |
| sensor_data_id | INTEGER | Sensör verisi ID |
| prediction | TEXT | Yapay zeka tahmini |
| recommendation | TEXT | Öneri |
| created_at | TIMESTAMP | Analiz zamanı |

---

## 🔗 Tablolar Arasındaki İlişkiler

- Bir kullanıcı birden fazla tarlaya sahip olabilir.
- Bir tarla birden fazla sensöre sahip olabilir.
- Bir sensör birçok veri üretebilir.
- Her sensör verisi için analiz sonucu oluşturulabilir.

İlişki yapısı:

Users → Fields → Sensors → Sensor_Data → Analysis

---

## ⚡ İndeksleme Stratejisi

Performansı artırmak için aşağıdaki alanlarda indeks kullanılacaktır:

- sensor_data.sensor_id
- sensor_data.created_at
- analysis.sensor_data_id

Bu indeksler sayesinde sensör verileri ve analiz sonuçları daha hızlı sorgulanabilecektir.

---

## 🚀 Performans ve Ölçeklenebilirlik

- Veriler ilişkisel yapı ile saklanacaktır.
- Gereksiz veri tekrarının önüne geçilecektir.
- İndeksleme sayesinde sorgu performansı artırılacaktır.
- Yeni sensör tipleri ve yeni analiz türleri sisteme kolayca eklenebilecektir.
- Veritabanı büyüdüğünde performans kaybı minimum seviyede tutulacaktır.

---

## ✅ Sonuç

Tasarlanan PostgreSQL veritabanı şeması, Akıllı Tarım Yönetim Sistemi için gerekli kullanıcı, sensör ve analiz verilerini güvenli ve performanslı şekilde saklayabilecek yapıdadır. İlişkiler, veri tipleri ve indeksleme stratejileri göz önünde bulundurularak ölçeklenebilir bir tasarım oluşturulmuştur.
