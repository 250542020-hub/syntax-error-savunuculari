from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-akilli-tarim-gizli-anahtar'
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'api',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tarim_projesi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'tarim_projesi' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.environ.get('DB_NAME',     'akilli_tarim_db'),
        'USER':     os.environ.get('DB_USER',     'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST':     os.environ.get('DB_HOST',     '127.0.0.1'),
        'PORT':     os.environ.get('DB_PORT',     '5432'),
        'CONN_MAX_AGE': 60,
        'CONN_HEALTH_CHECKS': True,
        'OPTIONS': {
            'connect_timeout': 5,
            'keepalives':          1,
            'keepalives_idle':    30,
            'keepalives_interval': 5,
            'keepalives_count':    5,
        },
    }
}

LANGUAGE_CODE = 'tr-tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# ──────────────────────────────────────────────────────────
# LOGLAMA YAPILANDIRMASI (Ceren Çam — Hafta 5)
# ──────────────────────────────────────────────────────────
# api/loglama_config.py içindeki LOGLAMA_AYARLARI sözlüğü
# buraya doğrudan kopyalandı. Import yapılırsa settings.py
# yüklenirken `api` modülü henüz tanınmıyor → ModuleNotFoundError
# olur (Hayat'ın 7. düzeltmesi). Bu yaklaşım her iki sorunu
# birden çözer: hem detaylı loglama aktif, hem import hatası yok.
# ──────────────────────────────────────────────────────────

LOG_KLASORU = os.path.join(BASE_DIR, "api", "logs")
os.makedirs(LOG_KLASORU, exist_ok=True)

LOGGING = {
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
# GÜVENLİK AYARLARI
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY' # Clickjacking koruması

# Token yetkilendirmesi için bunu INSTALLED_APPS'e ekle
# 'rest_framework.authtoken', 

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
# ──────────────────────────────────────────────────────────
# EK GUVENLIK AYARLARI (Gorev 2)
# ──────────────────────────────────────────────────────────

# Login / Logout yonlendirmeleri
LOGIN_URL = '/giris/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/giris/'

# Oturum (Session) guvenligi
SESSION_COOKIE_HTTPONLY = True       # JS oturum cerezine erisemez
SESSION_COOKIE_SAMESITE = 'Lax'      # CSRF saldirilarina karsi
SESSION_COOKIE_AGE = 60 * 60 * 2     # 2 saat sonra otomatik logout
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# CSRF cerezi guvenligi
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Production'da HTTPS zorla (DEBUG=False oldugunda otomatik aktif)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000   # 1 yil
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Sifre kalitesi dogrulayicilari
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
