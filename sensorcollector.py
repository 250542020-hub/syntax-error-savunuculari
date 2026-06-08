import os
import sys
import json
import time
import logging
import threading
import unittest
from datetime import datetime, timezone
from collections import deque
from unittest.mock import MagicMock

import paho.mqtt.client as mqtt
from psycopg2 import pool, OperationalError


# ──────────────────────────────────────────────────────────
# YAPILANDIRMA
# ──────────────────────────────────────────────────────────

MQTT_CONFIG = {
    "broker":    "localhost",
    "port":      1883,
    "topic":     "tarim/sensor/toprak_nemi",
    "client_id": "toprak_nemi_collector_001",
    "keepalive": 60,
}

DB_CONFIG = {
    "host":     os.environ.get("DB_HOST", "localhost"),
    "port":     int(os.environ.get("DB_PORT", 5432)),
    # Django ile AYNI veritabanı (akilli_tarim_db). Daha önce "tarim_db" yazılıydı,
    # var olmayan bir DB'ye baglanmak OperationalError'a yol aciyordu.
    "database": os.environ.get("DB_NAME", "akilli_tarim_db"),
    "user":     os.environ.get("DB_USER", "postgres"),
    # Sifre artik koda gomulu degil; ortam degiskeninden okunur.
    "password": os.environ.get("DB_PASSWORD", ""),
    # Baglanti hatalarina karsi: asili kalmayi onler + kopuk baglantiyi erken yakalar.
    "connect_timeout":     5,
    "keepalives":          1,
    "keepalives_idle":     30,
    "keepalives_interval": 5,
    "keepalives_count":    5,
}

# Havuz boyutlari ve yeniden baglanma denemesi ortam degiskeninden ayarlanabilir.
DB_POOL_MIN          = int(os.environ.get("DB_POOL_MIN", 1))
DB_POOL_MAX          = int(os.environ.get("DB_POOL_MAX", 5))
DB_RECONNECT_RETRIES = int(os.environ.get("DB_RECONNECT_RETRIES", 5))

FLUSH_INTERVAL_SECONDS = 300   # Her 5 dakikada bir veritabanına yaz
SULAMA_ESIGI = 30.0            # %30 altında sulama uyarısı


# ──────────────────────────────────────────────────────────
# LOGLAMA
# ──────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("toprak_nemi.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────
# VERİTABANI YÖNETİCİSİ
#
# Gerekli tablo:
#   CREATE TABLE toprak_nemi_olcumleri (
#       id          SERIAL PRIMARY KEY,
#       sensor_id   INTEGER NOT NULL,
#       toprak_nemi FLOAT   NOT NULL,
#       kayit_zamani TIMESTAMP NOT NULL
#   );
# ──────────────────────────────────────────────────────────

class DatabaseManager:

    def __init__(self, config: dict, minconn: int = DB_POOL_MIN, maxconn: int = DB_POOL_MAX):
        self.config  = config
        self.minconn = minconn
        self.maxconn = maxconn
        self._pool   = None
        # Havuz yeniden kurulurken iki thread'in ayni anda baglanmasini engeller.
        self._lock   = threading.Lock()
        self._connect()

    def _connect(self, retries: int = DB_RECONNECT_RETRIES):
        """
        Baglanti havuzunu kurar. Basarisiz olursa ustel geri cekilmeyle (exponential
        backoff) yeniden dener — DB acilista hazir degilse uygulama hemen olmesin.

        NOT: SimpleConnectionPool yerine ThreadedConnectionPool kullaniliyor; bu modul
        cok thread'li (MQTT loop + FlushScheduler + kapanista force_flush).
        """
        gecikme = 1
        for deneme in range(1, retries + 1):
            try:
                self._pool = pool.ThreadedConnectionPool(
                    self.minconn, self.maxconn, **self.config
                )
                logger.info(" Veritabanı bağlantı havuzu kuruldu (min=%d, max=%d).",
                            self.minconn, self.maxconn)
                return
            except OperationalError as e:
                logger.error(" Veritabanına bağlanılamadı (deneme %d/%d): %s",
                             deneme, retries, e)
                if deneme == retries:
                    raise
                time.sleep(gecikme)
                gecikme = min(gecikme * 2, 30)   # ustel geri cekilme, tavan 30 sn

    def _ensure_pool(self):
        """Havuz hic kurulmamis ya da kapanmissa (runtime'da DB dustuyse) yeniden kurar."""
        if self._pool is None or self._pool.closed:
            logger.warning(" Havuz kapali/yok — yeniden bağlanılıyor...")
            self._connect()

    def bulk_insert(self, records: list) -> int:
        """Toprak nemi kayıtlarını toplu olarak veritabanına yazar."""
        if not records:
            return 0

        insert_sql = """
            INSERT INTO toprak_nemi_olcumleri
                (sensor_id, toprak_nemi, kayit_zamani)
            VALUES
                (%(sensor_id)s, %(toprak_nemi)s, %(kayit_zamani)s)
        """

        with self._lock:
            self._ensure_pool()
            try:
                conn = self._pool.getconn()
            except pool.PoolError as e:
                # Tum baglantilar kullanimda → havuz tukendi.
                logger.error(" Bağlantı havuzu tükendi: %s", e)
                raise

        baglanti_bozuk = False
        try:
            with conn.cursor() as cur:
                cur.executemany(insert_sql, records)
            conn.commit()
            logger.info(" %d ölçüm veritabanına yazıldı.", len(records))
            return len(records)
        except Exception as e:
            baglanti_bozuk = True
            logger.error(" Veritabanı yazma hatası: %s", e)
            try:
                conn.rollback()
            except Exception as rb:
                # Baglanti tamamen kopmussa rollback de patlar; yutuyoruz.
                logger.warning(" Rollback başarısız (bağlantı kopmuş olabilir): %s", rb)
            raise
        finally:
            # Bozuk baglantiyi havuza GERI KOYMA, kapat (close=True). Aksi halde
            # bir sonraki getconn() olu baglanti dondurur ve hata zincirlenir.
            try:
                self._pool.putconn(conn, close=baglanti_bozuk)
            except pool.PoolError as e:
                logger.warning(" Bağlantı havuza iade edilemedi: %s", e)

    def close(self):
        if self._pool and not self._pool.closed:
            self._pool.closeall()
            logger.info(" Veritabanı bağlantıları kapatıldı.")


# ──────────────────────────────────────────────────────────
# BUFFER — Thread-safe bellek tamponu
# Veri kaybını önlemek için veriler 5 dakika bellekte
# bekletilir, sonra toplu olarak veritabanına yazılır.
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
#
# Beklenen mesaj formatı (JSON):
#   {
#     "sensor_id":   1,
#     "toprak_nemi": 42.5
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

            # Zorunlu alanları kontrol et
            record = {
                "sensor_id":    int(payload["sensor_id"]),
                "toprak_nemi":  float(payload["toprak_nemi"]),
                "kayit_zamani": datetime.now(timezone.utc),
            }

            self.buffer.add(record)
            logger.debug(f"📥 Veri alındı: {record}")

            # Sulama uyarısı
            if record["toprak_nemi"] < SULAMA_ESIGI:
                logger.warning(
                    f"  SULAMA GEREKLİ! "
                    f"Sensör {record['sensor_id']} → "
                    f"Toprak nemi: %{record['toprak_nemi']}"
                )

        except KeyError as e:
            logger.warning(f"  Eksik alan, mesaj atlandı → {msg.payload} | Hata: {e}")
        except (ValueError, json.JSONDecodeError) as e:
            logger.warning(f"  Geçersiz mesaj atlandı → {msg.payload} | Hata: {e}")

    def _on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.warning(f"  MQTT bağlantısı beklenmedik şekilde kesildi (rc={rc}).")


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
        logger.info(f"  Her {self.interval} saniyede bir veritabanına yazılacak.")

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
            # Veri kaybı önleme: başarısız kayıtları geri al
            logger.error(" Yazma başarısız — kayıtlar buffer'a geri alındı.")
            for r in records:
                self.buffer.add(r)

    def force_flush(self):
        """Kapatma sırasında kalan verileri zorla yazar."""
        logger.info(" Zorunlu flush yapılıyor...")
        self._flush()


# ──────────────────────────────────────────────────────────
# ANA UYGULAMA
# ──────────────────────────────────────────────────────────

class ToprakNemiCollectorApp:

    def __init__(self):
        self.buffer    = SensorBuffer()
        self.db        = DatabaseManager(DB_CONFIG)
        self.mqtt      = MQTTCollector(MQTT_CONFIG, self.buffer)
        self.scheduler = FlushScheduler(self.buffer, self.db, FLUSH_INTERVAL_SECONDS)

    def start(self):
        logger.info(" Toprak Nemi Veri Toplama Modülü başlatılıyor...")
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
        logger.info(" Sistem kapatılıyor...")
        self.scheduler.stop()
        self.scheduler.force_flush()   # Kalan verileri kaydet
        self.mqtt.stop()
        self.db.close()
        logger.info(" Sistem güvenle kapatıldı.")


# ──────────────────────────────────────────────────────────
# TESTLER — python toprak_nemi_collector.py --test
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
        """Doğru formatlı mesaj buffer'a eklenmeli."""
        payload = json.dumps({
            "sensor_id": 1,
            "toprak_nemi": 42.5
        }).encode()
        self.collector._on_message(None, None, self._msg(payload))
        self.assertEqual(self.buffer.size(), 1)

    def test_bozuk_json_atlanir(self):
        """Bozuk JSON buffer'a eklenmemeli."""
        self.collector._on_message(None, None, self._msg(b"{ bozuk {{{"))
        self.assertEqual(self.buffer.size(), 0)

    def test_eksik_toprak_nemi_atlanir(self):
        """toprak_nemi alanı eksikse mesaj atlanmalı."""
        payload = json.dumps({"sensor_id": 1}).encode()
        self.collector._on_message(None, None, self._msg(payload))
        self.assertEqual(self.buffer.size(), 0)

    def test_dusuk_nem_kaydedilir(self):
        """Düşük toprak nemi verisi yine de kaydedilmeli."""
        payload = json.dumps({
            "sensor_id": 1,
            "toprak_nemi": 22.3
        }).encode()
        self.collector._on_message(None, None, self._msg(payload))
        record = self.buffer.flush()[0]
        self.assertLess(record["toprak_nemi"], SULAMA_ESIGI)

    def test_sulama_esigi_ustu_kaydedilir(self):
        """Yeterli toprak nemi de kayıt edilmeli."""
        payload = json.dumps({
            "sensor_id": 2,
            "toprak_nemi": 55.0
        }).encode()
        self.collector._on_message(None, None, self._msg(payload))
        self.assertEqual(self.buffer.size(), 1)


class TestFlushScheduler(unittest.TestCase):

    def _ornek_kayit(self, n=5):
        return [
            {
                "sensor_id":    1,
                "toprak_nemi":  40.0,
                "kayit_zamani": datetime.now(timezone.utc)
            }
            for _ in range(n)
        ]

    def test_basarili_flush(self):
        """Flush sonrası buffer boşalmalı ve DB'ye yazılmalı."""
        buf = SensorBuffer()
        for r in self._ornek_kayit(10):
            buf.add(r)
        mock_db = MagicMock()
        mock_db.bulk_insert.return_value = 10
        s = FlushScheduler(buf, mock_db, interval=999)
        s.force_flush()
        mock_db.bulk_insert.assert_called_once()
        self.assertEqual(buf.size(), 0)

    def test_db_hatasinda_veri_kaybolmaz(self):
        """DB hatası durumunda veriler buffer'a geri dönmeli."""
        buf = SensorBuffer()
        for r in self._ornek_kayit(5):
            buf.add(r)
        mock_db = MagicMock()
        mock_db.bulk_insert.side_effect = Exception("DB bağlantı hatası")
        s = FlushScheduler(buf, mock_db, interval=999)
        s.force_flush()
        self.assertEqual(buf.size(), 5)  # Veriler kaybolmamalı

    def test_bos_buffer_flush(self):
        """Boş buffer'da flush hata vermemeli."""
        buf = SensorBuffer()
        mock_db = MagicMock()
        s = FlushScheduler(buf, mock_db, interval=999)
        s.force_flush()
        mock_db.bulk_insert.assert_not_called()


# ──────────────────────────────────────────────────────────
# ENTEGRASYON TESTLERİ — Gerçek PostgreSQL bağlantısı gerektirir
# Çalıştırmadan önce DB_CONFIG'i doldurun.
#   python toprak_nemi_collector.py --integration-test
#
# Bu testler:
#   1. Gerçek DB'ye bağlanır
#   2. Test tablosunu oluşturur
#   3. Veri yazar ve okur
#   4. Test tablosunu temizler
# ──────────────────────────────────────────────────────────

class TestEntegrasyon(unittest.TestCase):
    """
    Gerçek PostgreSQL bağlantısıyla entegrasyon testleri.
    DB_CONFIG'deki bilgiler doğru olmalıdır.
    """

    TEST_TABLO = "test_toprak_nemi_olcumleri"

    @classmethod
    def setUpClass(cls):
        """Test başlamadan önce test tablosunu oluştur."""
        try:
            import psycopg2
            cls.conn = psycopg2.connect(**DB_CONFIG)
            cls.conn.autocommit = True
            with cls.conn.cursor() as cur:
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {cls.TEST_TABLO} (
                        id           SERIAL PRIMARY KEY,
                        sensor_id    INTEGER   NOT NULL,
                        toprak_nemi  FLOAT     NOT NULL,
                        kayit_zamani TIMESTAMP NOT NULL
                    )
                """)
            logger.info(f" Test tablosu oluşturuldu: {cls.TEST_TABLO}")
        except Exception as e:
            raise unittest.SkipTest(f"DB bağlantısı kurulamadı, test atlandı: {e}")

    @classmethod
    def tearDownClass(cls):
        """Tüm testler bittikten sonra test tablosunu sil."""
        try:
            with cls.conn.cursor() as cur:
                cur.execute(f"DROP TABLE IF EXISTS {cls.TEST_TABLO}")
            cls.conn.close()
            logger.info(f" Test tablosu silindi: {cls.TEST_TABLO}")
        except Exception as e:
            logger.warning(f"Test tablosu silinemedi: {e}")

    def setUp(self):
        """Her testten önce tabloyu temizle."""
        with self.conn.cursor() as cur:
            cur.execute(f"DELETE FROM {self.TEST_TABLO}")

    def _db_manager(self):
        """Test tablosunu kullanan özel bir DatabaseManager döndürür."""
        # Orijinal insert_sql'i geçici olarak test tablosuna yönlendir
        db = DatabaseManager.__new__(DatabaseManager)
        db.config = DB_CONFIG
        import psycopg2.pool as pg_pool
        db._pool = pg_pool.SimpleConnectionPool(minconn=1, maxconn=2, **DB_CONFIG)
        db._test_tablo = self.TEST_TABLO
        return db

    def _insert_test(self, db, records):
        """Test tablosuna yazar (bulk_insert'in test versiyonu)."""
        insert_sql = f"""
            INSERT INTO {self.TEST_TABLO}
                (sensor_id, toprak_nemi, kayit_zamani)
            VALUES
                (%(sensor_id)s, %(toprak_nemi)s, %(kayit_zamani)s)
        """
        conn = db._pool.getconn()
        try:
            with conn.cursor() as cur:
                cur.executemany(insert_sql, records)
            conn.commit()
            return len(records)
        finally:
            db._pool.putconn(conn)

    def _kayit_sayisi(self):
        """Test tablosundaki kayıt sayısını döndürür."""
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {self.TEST_TABLO}")
            return cur.fetchone()[0]

    # ── Test 1 ──────────────────────────────────────────────
    def test_tekil_kayit_yazilir(self):
        """Tek bir toprak nemi kaydı doğru yazılmalı."""
        db = self._db_manager()
        kayit = [{
            "sensor_id":    1,
            "toprak_nemi":  45.5,
            "kayit_zamani": datetime.now(timezone.utc),
        }]
        self._insert_test(db, kayit)
        self.assertEqual(self._kayit_sayisi(), 1)
        db._pool.closeall()

    # ── Test 2 ──────────────────────────────────────────────
    def test_toplu_kayit_yazilir(self):
        """10 kayıt toplu olarak doğru yazılmalı."""
        db = self._db_manager()
        kayitlar = [
            {
                "sensor_id":    i % 5 + 1,
                "toprak_nemi":  round(20.0 + i * 2.5, 1),
                "kayit_zamani": datetime.now(timezone.utc),
            }
            for i in range(10)
        ]
        self._insert_test(db, kayitlar)
        self.assertEqual(self._kayit_sayisi(), 10)
        db._pool.closeall()

    # ── Test 3 ──────────────────────────────────────────────
    def test_yazilan_deger_dogru_okunur(self):
        """Yazılan toprak nemi değeri doğru geri okunmalı."""
        db = self._db_manager()
        beklenen_nem = 38.7
        kayit = [{
            "sensor_id":    3,
            "toprak_nemi":  beklenen_nem,
            "kayit_zamani": datetime.now(timezone.utc),
        }]
        self._insert_test(db, kayit)

        with self.conn.cursor() as cur:
            cur.execute(
                f"SELECT toprak_nemi FROM {self.TEST_TABLO} WHERE sensor_id = 3"
            )
            okunan_nem = cur.fetchone()[0]

        self.assertAlmostEqual(okunan_nem, beklenen_nem, places=1)
        db._pool.closeall()

    # ── Test 4 ──────────────────────────────────────────────
    def test_sulama_esigi_altindaki_kayitlar(self):
        """Sulama eşiği altındaki kayıtlar sorgulanabilmeli."""
        db = self._db_manager()
        kayitlar = [
            {"sensor_id": 1, "toprak_nemi": 22.0, "kayit_zamani": datetime.now(timezone.utc)},
            {"sensor_id": 2, "toprak_nemi": 55.0, "kayit_zamani": datetime.now(timezone.utc)},
            {"sensor_id": 3, "toprak_nemi": 18.5, "kayit_zamani": datetime.now(timezone.utc)},
        ]
        self._insert_test(db, kayitlar)

        with self.conn.cursor() as cur:
            cur.execute(
                f"SELECT COUNT(*) FROM {self.TEST_TABLO} WHERE toprak_nemi < %s",
                (SULAMA_ESIGI,)
            )
            sulama_gereken = cur.fetchone()[0]

        self.assertEqual(sulama_gereken, 2)
        db._pool.closeall()

    # ── Test 5 ──────────────────────────────────────────────
    def test_bos_kayit_listesi_hata_vermez(self):
        """Boş liste gönderildiğinde hata oluşmamalı."""
        db = self._db_manager()
        sonuc = self._insert_test(db, [])
        self.assertEqual(sonuc, 0)
        self.assertEqual(self._kayit_sayisi(), 0)
        db._pool.closeall()


# ──────────────────────────────────────────────────────────
# TEST VERİSİ YAYINCISI — Gerçek sensör olmadan test için
# Ayrı bir terminalde çalıştırın:
#   python toprak_nemi_collector.py --simulate
# ──────────────────────────────────────────────────────────

def run_simulator():
    import random
    logger.info(" Test simülatörü başlatılıyor...")
    client = mqtt.Client(client_id="test_simulator")
    client.connect(MQTT_CONFIG["broker"], MQTT_CONFIG["port"])
    client.loop_start()
    try:
        while True:
            veri = {
                "sensor_id":   random.randint(1, 5),
                "toprak_nemi": round(random.uniform(15, 70), 1),
            }
            client.publish(MQTT_CONFIG["topic"], json.dumps(veri))
            logger.info(f" Test verisi gönderildi: {veri}")
            time.sleep(5)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
        logger.info(" Simülatör durduruldu.")


# ──────────────────────────────────────────────────────────
# GİRİŞ NOKTASI
# ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--test" in sys.argv:
        sys.argv.remove("--test")
        # Entegrasyon testlerini hariç tut, sadece unit testleri çalıştır
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        suite.addTests(loader.loadTestsFromTestCase(TestSensorBuffer))
        suite.addTests(loader.loadTestsFromTestCase(TestMQTTParsing))
        suite.addTests(loader.loadTestsFromTestCase(TestFlushScheduler))
        print(" Unit testler çalıştırılıyor...\n")
        unittest.TextTestRunner(verbosity=2).run(suite)

    elif "--integration-test" in sys.argv:
        # Sadece entegrasyon testlerini çalıştır (gerçek DB gerektirir)
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestEntegrasyon)
        print(" Entegrasyon testleri çalıştırılıyor (gerçek DB gerektirir)...\n")
        unittest.TextTestRunner(verbosity=2).run(suite)

    elif "--simulate" in sys.argv:
        run_simulator()

    else:
        app = ToprakNemiCollectorApp()
        app.start()
