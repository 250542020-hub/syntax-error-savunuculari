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
