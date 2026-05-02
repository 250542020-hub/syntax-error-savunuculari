import logging
import traceback
from datetime import datetime
from django.http import JsonResponse

logger = logging.getLogger("api.error_handler")


def hata_yaniti_olustur(hata_kodu: str, mesaj: str, detaylar: list = None, http_durum: int = 400) -> JsonResponse:
    yanit_govde = {
        "basarili": False,
        "hata_kodu": hata_kodu,
        "mesaj": mesaj,
        "detaylar": detaylar or [],
        "zaman_damgasi": datetime.now().isoformat(timespec="seconds"),
    }
    logger.error("API Hata Yaniti | hata_kodu=%s | http=%d | mesaj=%s", hata_kodu, http_durum, mesaj)
    return JsonResponse(yanit_govde, status=http_durum)


def basari_yaniti_olustur(veri: dict, uyarilar: list = None) -> JsonResponse:
    yanit_govde = {
        "basarili": True,
        "veri": veri,
        "uyarilar": uyarilar or [],
        "zaman_damgasi": datetime.now().isoformat(timespec="seconds"),
    }
    if uyarilar:
        logger.warning("Basarili yanit - uyarilar mevcut | uyarilar=%s", uyarilar)
    else:
        logger.info("Basarili yanit gonderildi | veri_anahtarlari=%s", list(veri.keys()))
    return JsonResponse(yanit_govde, status=200)


def dogrulama_hatalarini_isle(dogrulama_sonucu: dict):
    if dogrulama_sonucu["gecerli"]:
        return None
    return hata_yaniti_olustur(
        hata_kodu="DOGRULAMA_HATASI",
        mesaj="Gonderilen veri dogrulama kontrollerinden gecemedi.",
        detaylar=dogrulama_sonucu["hatalar"],
        http_durum=422,
    )


def beklenmeyen_hatayi_isle(hata: Exception, islem_adi: str = "bilinmiyor") -> JsonResponse:
    logger.critical("Beklenmeyen hata | islem=%s | hata_tipi=%s | mesaj=%s\nStack Trace:\n%s",
                    islem_adi, type(hata).__name__, str(hata), traceback.format_exc())
    return hata_yaniti_olustur(
        hata_kodu="SUNUCU_HATASI",
        mesaj="Sunucu tarafinda beklenmeyen bir hata olustu. Lutfen tekrar deneyin.",
        http_durum=500,
    )


def dis_servis_hatasini_isle(servis_adi: str, hata: Exception) -> JsonResponse:
    logger.error("Dis servis baglanti hatasi | servis=%s | hata=%s", servis_adi, str(hata))
    return hata_yaniti_olustur(
        hata_kodu="DIS_SERVIS_HATASI",
        mesaj=f"'{servis_adi}' servisine ulasilamiyor. Lutfen daha sonra tekrar deneyin.",
        detaylar=[str(hata)],
        http_durum=503,
    )
