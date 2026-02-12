import os
from config.settings import BASE_DIR

_engine = os.environ.get("DJANGO_DB_ENGINE", "django.db.backends.sqlite3").strip()
_name = os.environ.get("DJANGO_DB_NAME", os.path.join(BASE_DIR, "..", "db.sqlite3")).strip()

DATABASES = {
    "default": {
        "ENGINE": _engine,
        "NAME": _name,
    }
}

_user = os.environ.get("DJANGO_DB_USER", "").strip()
_password = os.environ.get("DJANGO_DB_PASSWORD", "").strip()
_host = os.environ.get("DJANGO_DB_HOST", "").strip()
_port = os.environ.get("DJANGO_DB_PORT", "").strip()

if _user:
    DATABASES["default"]["USER"] = _user
if _password:
    DATABASES["default"]["PASSWORD"] = _password
if _host:
    DATABASES["default"]["HOST"] = _host
if _port:
    DATABASES["default"]["PORT"] = _port

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
