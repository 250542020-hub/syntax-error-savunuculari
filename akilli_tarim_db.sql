-- 1. Tarlalar Tablosu (Eşik değeri dahil)
CREATE TABLE tarlalar (
    id SERIAL PRIMARY KEY,
    tarla_adi VARCHAR(100) NOT NULL,
    konum VARCHAR(255),
    sulama_esigi DECIMAL(5, 2) DEFAULT 30.0, 
    olusturma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Sensörler Tablosu
CREATE TABLE sensorler (
    id SERIAL PRIMARY KEY,
    tarla_id INT REFERENCES tarlalar(id) ON DELETE CASCADE,
    sensor_tipi VARCHAR(50) NOT NULL,
    durum BOOLEAN DEFAULT TRUE,
    son_gorulme TIMESTAMP
);

-- 3. Ölçümler Tablosu (Veri akışı ve AI için)
CREATE TABLE olcumler (
    id BIGSERIAL PRIMARY KEY,
    sensor_id INT REFERENCES sensorler(id) ON DELETE CASCADE,
    sicaklik DECIMAL(5, 2),
    nem DECIMAL(5, 2),
    toprak_nemi DECIMAL(5, 2),
    hava_durumu VARCHAR(50),
    kayit_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

