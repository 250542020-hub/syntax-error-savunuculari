import requests
import time
import random

API_URL = "http://127.0.0.1:8000/api/sensor-data/"

print("Akıllı Tarım Simülatörü Başlatıldı...")

while True:
    # Rastgele ama mantıklı veriler üretelim
    payload = {
        "device_id": "SENSOR_01",
        "temperature": round(random.uniform(20.0, 35.0), 2),
        "humidity": round(random.uniform(40.0, 60.0), 2),
        "soil_moisture": round(random.uniform(10.0, 80.0), 2)
    }

    try:
        response = requests.post(API_URL, json=payload)
        res_data = response.json()
        print(f"Gönderilen: {payload} | Sunucu Cevabı: {res_data['karar']}")
    except Exception as e:
        print("Hata: Sunucu kapalı mı?", e)

    time.sleep(5) # 5 saniyede bir veri gönder