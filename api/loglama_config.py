import os

LOG_KLASORU = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "api", "logs")
os.makedirs(LOG_KLASORU, exist_ok=True)

LOGLAMA_AYARLARI = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "ayrintili": {
            "format": "[%(asctime)s] %(levelname)-8s %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "kisa": {
            "format": "%(levelname)-8s %(name)s | %(message)s",
        },
    },
    "handlers": {
        "terminal": {
            "class": "logging.StreamHandler",
            "formatter": "kisa",
            "level": "DEBUG",
        },
        "dosya_genel": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_KLASORU, "api_genel.log"),
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,
            "encoding": "utf-8",
            "formatter": "ayrintili",
            "level": "INFO",
        },
        "dosya_hatalar": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_KLASORU, "api_hatalar.log"),
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,
            "encoding": "utf-8",
            "formatter": "ayrintili",
            "level": "ERROR",
        },
    },
    "loggers": {
        "api": {
            "handlers": ["terminal", "dosya_genel", "dosya_hatalar"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django": {
            "handlers": ["terminal", "dosya_genel"],
            "level": "WARNING",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["terminal"],
        "level": "WARNING",
    },
}
