import sys
import json
import time
import logging
import threading
import unittest
from datetime import datetime
from collections import deque
from unittest.mock import MagicMock

import paho.mqtt.client as mqtt
from psycopg2 import pool, OperationalError


# ──────────────────────────────────────────────────────────
# YAPILANDIRMA  ← Kendi bilgilerinizle doldurun
# ──────────────────────────────────────────────────────────

MQTT_CONFIG = {
    "broker":    "localhost",
    "port":      1883,
    "topic":     "tarim/sensor/olcum",
    "client_id": "sensor_collector_001",
    "keepalive": 60,
}

DB_CONFIG = {
    "port":     5432,
    "database": "tarim_db",   # ← PostgreSQL DB adınız
    "user":     "postgres",
    "password": "sifreniz",   # ← PostgreSQL şifreniz
}

FLUSH_INTERVAL_SECONDS = 300  # 5 dakika


# ──────────────────────────────────────────────────────────
# LOGLAMA
# ──────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("sensor_collector.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────
# VERİTABANI YÖNETİCİSİ
# Tablo: olcumler (sensor_id, sicaklik, nem, toprak_nemi,
#                  hava_durumu, kayit_zamani)
# Tablo: sensorler → son_gorulme güncellenir
# ──────────────────────────────────────────────────────────

class DatabaseManager:

    def __init__(self, config: dict):
        self.config = config
        self._pool = None
        self._connect()

    def _connect(self):
        try:
            self._pool = pool.SimpleConnectionPool(minconn=1, maxconn=5, **self.config)
            logger.info(" Veritabanı bağlantısı kuruldu.")
        except OperationalError as e:
            logger.error(f" Veritabanına bağlanılamadı: {e}")
            raise

    def bulk_insert(self, records: list) -> int:
        if not records:
            return 0

        update_sql = """
            UPDATE sensorler
               SET son_gorulme = %(kayit_zamani)s
             WHERE id = %(sensor_id)s
        """
        insert_sql = """
            INSERT INTO olcumler
                (sensor_id, sicaklik, nem, toprak_nemi, hava_durumu, kayit_zamani)
            VALUES
                (%(sensor_id)s, %(sicaklik)s, %(nem)s,
                 %(toprak_nemi)s, %(hava_durumu)s, %(kayit_zamani)s)
        """
        conn = self._pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.executemany(update_sql, records)
                cur.executemany(insert_sql, records)
            conn.commit()
            logger.info(f" {len(records)} ölçüm veritabanına yazıldı.")
            return len(records)
        except Exception as e:
            conn.rollback()
            logger.error(f" Yazma hatası: {e}")
            raise
        finally:
            self._pool.putconn(conn)

    def close(self):
        if self._pool:
            self._pool.closeall()
            logger.info(" Veritabanı bağlantıları kapatıldı.")


# ──────────────────────────────────────────────────────────
# BUFFER — Thread-safe bellek tamponu
# ──────────────────────────────────────────────────────────

class SensorBuffer:

    def __init__(self):
        self._buffer: deque = deque()
        self._lock = threading.Lock()

    def add(self, record: dict):
        with self._lock:
            self._buffer.append(record)

    def flush(self) -> list:
        with self._lock:
            records = list(self._buffer)
            self._buffer.clear()
        return records

    def size(self) -> int:
        with self._lock:
            return len(self._buffer)


# ──────────────────────────────────────────────────────────
# MQTT YÖNETİCİSİ
# Beklenen mesaj formatı (JSON):
#   {
#     "sensor_id":   1,
#     "sicaklik":    25.3,
#     "nem":         60.0,
#     "toprak_nemi": 42.5,
#     "hava_durumu": "Güneşli"
#   }
# ──────────────────────────────────────────────────────────

class MQTTCollector:

    def __init__(self, config: dict, buffer: SensorBuffer):
        self.config = config
        self.buffer = buffer
        self.client = mqtt.Client(client_id=config["client_id"])
        self.client.on_connect    = self._on_connect
        self.client.on_message    = self._on_message
        self.client.on_disconnect = self._on_disconnect

    def connect(self):
        try:
            self.client.connect(
                self.config["broker"],
                self.config["port"],
                self.config["keepalive"],
            )
            logger.info(" MQTT broker'a bağlanıldı.")
        except Exception as e:
            logger.error(f" MQTT bağlantı hatası: {e}")
            raise

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        logger.info(" MQTT bağlantısı kapatıldı.")

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            client.subscribe(self.config["topic"])
            logger.info(f" Topic dinleniyor: {self.config['topic']}")
        else:
            logger.error(f" MQTT bağlantı reddedildi. Kod: {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            record = {
                "sensor_id":    int(payload["sensor_id"]),
                "sicaklik":     float(payload.get("sicaklik", 0)),
                "nem":          float(payload.get("nem", 0)),
                "toprak_nemi":  float(payload["toprak_nemi"]),
                "hava_durumu":  payload.get("hava_durumu", None),
                "kayit_zamani": datetime.utcnow(),
            }
            self.buffer.add(record)

            if record["toprak_nemi"] < 30.0:
                logger.warning(
                    f"  SULAMA GEREKLİ! Sensör {record['sensor_id']} → "
                    f"Toprak nemi: %{record['toprak_nemi']}"
                )
            logger.debug(f" Veri alındı: {record}")

        except (KeyError, ValueError, json.JSONDecodeError) as e:
            logger.warning(f"  Geçersiz mesaj atlandı → {msg.payload} | Hata: {e}")

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning(f"  MQTT bağlantısı kesildi (rc={rc}).")


# ──────────────────────────────────────────────────────────
# ZAMANLAYICI — Her 5 dakikada buffer → veritabanı
# ──────────────────────────────────────────────────────────

class FlushScheduler:

    def __init__(self, buffer: SensorBuffer, db: DatabaseManager, interval: int):
        self.buffer   = buffer
        self.db       = db
        self.interval = interval
        self._stop    = threading.Event()
        self._thread  = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self._thread.start()
        logger.info(f"  Her {self.interval}s'de bir veritabanına yazılacak.")

    def stop(self):
        self._stop.set()
        self._thread.join(timeout=10)

    def _run(self):
        while not self._stop.wait(self.interval):
            self._flush()

    def _flush(self):
        records = self.buffer.flush()
        if not records:
            logger.info("  Buffer boş, yazılacak veri yok.")
            return
        try:
            self.db.bulk_insert(records)
        except Exception:
            # Veri kaybı önleme: kayıtları geri al
            logger.error(" Yazma başarısız — kayıtlar buffer'a geri alındı.")
            for r in records:
                self.buffer.add(r)

    def force_flush(self):
        logger.info(" Zorunlu flush yapılıyor...")
        self._flush()


# ──────────────────────────────────────────────────────────
# ANA UYGULAMA
# ──────────────────────────────────────────────────────────

class SensorCollectorApp:

    def __init__(self):
        self.buffer    = SensorBuffer()
        self.db        = DatabaseManager(DB_CONFIG)
        self.mqtt      = MQTTCollector(MQTT_CONFIG, self.buffer)
        self.scheduler = FlushScheduler(self.buffer, self.db, FLUSH_INTERVAL_SECONDS)

    def start(self):
        logger.info(" Sensör Veri Toplama Modülü başlatılıyor...")
        self.mqtt.connect()
        self.mqtt.start()
        self.scheduler.start()
        logger.info(" Sistem hazır. Ctrl+C ile durdurabilirsiniz.")
        try:
            while True:
                time.sleep(30)
                logger.info(f" Bekleyen kayıt sayısı: {self.buffer.size()}")
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        logger.info(" Kapatılıyor...")
        self.scheduler.stop()
        self.scheduler.force_flush()
        self.mqtt.stop()
        self.db.close()
        logger.info(" Sistem güvenle kapatildi.")


# ──────────────────────────────────────────────────────────
# TESTLER — python sensor_collector.py --test
# ──────────────────────────────────────────────────────────

class TestSensorBuffer(unittest.TestCase):

    def test_veri_ekleme_ve_boyut(self):
        buf = SensorBuffer()
        buf.add({"toprak_nemi": 45.0})
        buf.add({"toprak_nemi": 50.0})
        self.assertEqual(buf.size(), 2)

    def test_flush_sonrasi_buffer_bos(self):
        buf = SensorBuffer()
        buf.add({"toprak_nemi": 30.0})
        records = buf.flush()
        self.assertEqual(len(records), 1)
        self.assertEqual(buf.size(), 0)

    def test_coklu_thread_guvenli(self):
        buf = SensorBuffer()
        threads = [
            threading.Thread(target=buf.add, args=({"toprak_nemi": i},))
            for i in range(50)
        ]
        for t in threads: t.start()
        for t in threads: t.join()
        self.assertEqual(buf.size(), 50)


class TestMQTTParsing(unittest.TestCase):

    def setUp(self):
        self.buffer = SensorBuffer()
        self.collector = MQTTCollector.__new__(MQTTCollector)
        self.collector.buffer = self.buffer

    def _msg(self, payload: bytes):
        m = MagicMock()
        m.payload = payload
        return m

    def test_gecerli_mesaj_islenir(self):
        payload = json.dumps({
            "sensor_id": 1, "sicaklik": 25.0,
            "nem": 60.0, "toprak_nemi": 42.5
        }).encode()
        self.collector._on_message(None, None, self._msg(payload))
        self.assertEqual(self.buffer.size(), 1)

    def test_bozuk_json_atlanir(self):
        self.collector._on_message(None, None, self._msg(b"{ bozuk {{{"))
        self.assertEqual(self.buffer.size(), 0)

    def test_eksik_alan_atlanir(self):
        payload = json.dumps({"sensor_id": 1, "sicaklik": 25.0}).encode()
        self.collector._on_message(None, None, self._msg(payload))
        self.assertEqual(self.buffer.size(), 0)

    def test_dusuk_nem_kaydedilir(self):
        payload = json.dumps({
            "sensor_id": 1, "toprak_nemi": 22.3,
            "sicaklik": 30.0, "nem": 55.0
        }).encode()
        self.collector._on_message(None, None, self._msg(payload))
        record = self.buffer.flush()[0]
        self.assertLess(record["toprak_nemi"], 30.0)


class TestFlushScheduler(unittest.TestCase):

    def _sample_records(self, n=5):
        return [
            {"sensor_id": 1, "sicaklik": 25.0, "nem": 60.0,
             "toprak_nemi": 40.0, "hava_durumu": None,
             "kayit_zamani": datetime.utcnow()}
            for _ in range(n)
        ]

    def test_basarili_flush(self):
        buf = SensorBuffer()
        for r in self._sample_records(10):
            buf.add(r)
        mock_db = MagicMock()
        mock_db.bulk_insert.return_value = 10
        s = FlushScheduler(buf, mock_db, interval=999)
        s.force_flush()
        mock_db.bulk_insert.assert_called_once()
        self.assertEqual(buf.size(), 0)

    def test_db_hatasinda_veri_kaybolmaz(self):
        buf = SensorBuffer()
        for r in self._sample_records(5):
            buf.add(r)
        mock_db = MagicMock()
        mock_db.bulk_insert.side_effect = Exception("DB hatası")
        s = FlushScheduler(buf, mock_db, interval=999)
        s.force_flush()
        self.assertEqual(buf.size(), 5)  # Geri alınmış olmalı


# ──────────────────────────────────────────────────────────
# GİRİŞ NOKTASI
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--test" in sys.argv:
        sys.argv.remove("--test")
        print(" Testler çaliştiriliyor...\n")
        unittest.main(verbosity=2)
    else:
        app = SensorCollectorApp()
        app.start()
