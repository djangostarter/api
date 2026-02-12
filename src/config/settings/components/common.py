import os

from config.settings import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-starter-api-insecure-dev-key")

# SECURITY WARNING: don't run with debug turned on in production!
# 读取环境变量判断是否开启Debug模式，无须手动设置
_debug_raw = os.environ.get("DJANGO_DEBUG", os.environ.get("DEBUG", "true")).strip().lower()
DEBUG = _debug_raw in {"1", "true", "yes", "y", "on"}

# 读取环境变量判断是否docker环境，无须手动设置
DOCKER = os.environ.get('ENVIRONMENT', 'default') == 'docker'

URL_PREFIX = ""

_allowed_hosts_raw = os.environ.get("DJANGO_ALLOWED_HOSTS", "").strip()
if _allowed_hosts_raw:
    ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts_raw.split(",") if h.strip()]
else:
    ALLOWED_HOSTS = ["*"] if DEBUG else []

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

_trust_xff_raw = os.environ.get("DJANGO_TRUST_X_FORWARDED_FOR", "false").strip().lower()
TRUST_X_FORWARDED_FOR = _trust_xff_raw in {"1", "true", "yes", "y", "on"}


