import logging

logger = logging.getLogger("api.validators")

SENSOR_ALAN_SINIRLARI = {
    "temperature":   {"min": -10.0, "max": 60.0,  "tip": float},
    "humidity":      {"min": 0.0,   "max": 100.0, "tip": float},
    "soil_moisture": {"min": 0.0,   "max": 100.0, "tip": float},
}

SENSOR_ZORUNLU_ALANLAR = ["device_id", "temperature", "humidity", "soil_moisture"]


# ──────────────────────────────────────────────────────────
# ORTAK YARDIMCILAR
# Sensor ve hava durumu dogrulamasinda ayni kontrol mantigi
# tekrarlaniyordu; tek yere toplandi (kod tekrari azaltildi).
# ──────────────────────────────────────────────────────────

def _eksik_zorunlu_alanlar(veri: dict, zorunlu_alanlar: list) -> list:
    """Veride bulunmayan zorunlu alanlarin listesini doner."""
    return [alan for alan in zorunlu_alanlar if alan not in veri]


def _aralik_hatasi(alan: str, deger, sinir: dict):
    """
    Bir alanin sayisal tip ve [min, max] araligi kontrolu.
    Hata varsa aciklama metni, deger gecerliyse None doner.
    """
    if not isinstance(deger, (int, float)):
        return f"'{alan}' alani sayisal olmali; gelen tip: {type(deger).__name__}"
    if deger < sinir["min"] or deger > sinir["max"]:
        return f"'{alan}' degeri ({deger}) gecerli aralik disinda [{sinir['min']} - {sinir['max']}]"
    return None


def sensor_verisini_dogrula(veri: dict) -> dict:
    hatalar = []
    uyarilar = []

    eksikler = _eksik_zorunlu_alanlar(veri, SENSOR_ZORUNLU_ALANLAR)
    if eksikler:
        hatalar = [f"Zorunlu alan eksik: '{alan}'" for alan in eksikler]
        logger.warning("Sensor verisi zorunlu alan eksikligi | device_id=%s | hatalar=%s",
                       veri.get("device_id", "BILINMIYOR"), hatalar)
        return {"gecerli": False, "hatalar": hatalar, "uyarilar": uyarilar}

    for alan, sinir in SENSOR_ALAN_SINIRLARI.items():
        hata = _aralik_hatasi(alan, veri[alan], sinir)
        if hata:
            hatalar.append(hata)
            continue
        # Deger gecerli aralikta; kritik esik uyarilarini uret.
        deger = veri[alan]
        if alan == "soil_moisture" and deger < 15.0:
            uyarilar.append(f"Toprak nemi kritik seviyede dusuk: {deger}%")
        if alan == "temperature" and deger > 40.0:
            uyarilar.append(f"Sicaklik asiri yuksek: {deger} derece")

    device_id = veri.get("device_id", "")
    if not isinstance(device_id, str) or len(device_id.strip()) == 0:
        hatalar.append("'device_id' bos olamaz ve metin tipinde olmalidir")

    gecerli = len(hatalar) == 0
    if gecerli:
        logger.info("Sensor verisi gecerli | device_id=%s", veri.get("device_id"))
    else:
        logger.error("Sensor verisi GECERSIZ | device_id=%s | hatalar=%s",
                     veri.get("device_id", "BILINMIYOR"), hatalar)

    return {"gecerli": gecerli, "hatalar": hatalar, "uyarilar": uyarilar}


HAVA_DURUMU_ZORUNLU_ALANLAR = ["temperature", "humidity", "description", "city"]
HAVA_DURUMU_SINIRLARI = {
    "temperature": {"min": -50.0, "max": 70.0},
    "humidity":    {"min": 0.0,   "max": 100.0},
}


def hava_durumu_cevabini_dogrula(cevap: dict) -> dict:
    hatalar = []
    uyarilar = []

    eksikler = _eksik_zorunlu_alanlar(cevap, HAVA_DURUMU_ZORUNLU_ALANLAR)
    if eksikler:
        hatalar = [f"Hava durumu cevabinda zorunlu alan yok: '{alan}'" for alan in eksikler]
        logger.warning("Hava durumu API cevabi eksik alan | hatalar=%s", hatalar)
        return {"gecerli": False, "hatalar": hatalar, "uyarilar": uyarilar}

    for alan, sinir in HAVA_DURUMU_SINIRLARI.items():
        hata = _aralik_hatasi(alan, cevap.get(alan), sinir)
        if hata:
            hatalar.append(hata)

    description = cevap.get("description", "")
    if not isinstance(description, str) or len(description.strip()) == 0:
        hatalar.append("'description' bos olamaz")

    gecerli = len(hatalar) == 0
    if gecerli:
        logger.info("Hava durumu API cevabi gecerli | sehir=%s", cevap.get("city"))
    else:
        logger.error("Hava durumu API cevabi GECERSIZ | hatalar=%s", hatalar)

    return {"gecerli": gecerli, "hatalar": hatalar, "uyarilar": uyarilar}


def genel_cevap_dogrula(cevap, http_durum_kodu: int) -> dict:
    hatalar = []
    uyarilar = []

    if http_durum_kodu == 200:
        pass
    elif http_durum_kodu == 400:
        hatalar.append("Hatali istek (HTTP 400): Gonderilen veri gecersiz")
    elif http_durum_kodu == 401:
        hatalar.append("Yetkisiz erisim (HTTP 401): API anahtari gecersiz veya eksik")
    elif http_durum_kodu == 403:
        hatalar.append("Erisim reddedildi (HTTP 403): Bu kaynaga erisim izni yok")
    elif http_durum_kodu == 404:
        hatalar.append("Kaynak bulunamadi (HTTP 404): Endpoint mevcut degil")
    elif http_durum_kodu == 429:
        uyarilar.append("Istek limiti asildi (HTTP 429): Biraz bekleyip tekrar deneyin")
    elif http_durum_kodu >= 500:
        hatalar.append(f"Sunucu hatasi (HTTP {http_durum_kodu}): Servis su an yanit veremiyor")
    else:
        uyarilar.append(f"Beklenmeyen HTTP durum kodu: {http_durum_kodu}")

    gecerli = len(hatalar) == 0
    if gecerli:
        logger.info("Genel API cevap dogrulama | HTTP=%d | gecerli=True", http_durum_kodu)
    else:
        logger.error("Genel API cevap dogrulama | HTTP=%d | hatalar=%s", http_durum_kodu, hatalar)

    return {"gecerli": gecerli, "hatalar": hatalar, "uyarilar": uyarilar}
