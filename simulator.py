import requests
import time
import random
import os
import sys

API_URL = "http://127.0.0.1:8000/api/sensor-data/"
TOKEN_URL = "http://127.0.0.1:8000/api/token/"

# Token'i ortam degiskeninden al, yoksa kullanici adi/sifre ile alalim
TOKEN = os.environ.get('SIMULATOR_TOKEN')
USERNAME = os.environ.get('SIMULATOR_USER', 'simulator_user')
PASSWORD = os.environ.get('SIMULATOR_PASSWORD')

if not TOKEN:
    if not PASSWORD:
        print("Hata: SIMULATOR_TOKEN veya SIMULATOR_PASSWORD ortam degiskenini ayarla.")
        sys.exit(1)
    try:
        r = requests.post(TOKEN_URL, json={"username": USERNAME, "password": PASSWORD}, timeout=5)
        r.raise_for_status()
        TOKEN = r.json()['token']
        print(f"Token alindi: {TOKEN[:10]}...")
    except Exception as e:
        print(f"Token alinamadi: {e}")
        sys.exit(1)

HEADERS = {"Authorization": f"Token {TOKEN}"}

print("Akilli Tarim Simulatoru Baslatildi (Yetkilendirilmis)...")

while True:
    payload = {
        "device_id": "SENSOR_01",
        "temperature": round(random.uniform(20.0, 35.0), 2),
        "humidity": round(random.uniform(40.0, 60.0), 2),
        "soil_moisture": round(random.uniform(10.0, 80.0), 2),
    }
    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS, timeout=5)
        if response.status_code == 401:
            print("HATA: Token gecersiz veya suresi dolmus.")
            break
        res_data = response.json()
        print(f"Gonderilen: {payload} | Cevap: {res_data.get('karar', res_data)}")
    except Exception as e:
        print("Hata:", e)
    time.sleep(5)