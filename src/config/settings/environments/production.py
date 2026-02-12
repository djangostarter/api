import os


def _require(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


DEBUG = False

_require("DJANGO_SECRET_KEY")
_require("DJANGO_JWT_SALT")
_require("DJANGO_ALLOWED_HOSTS")

ALLOWED_HOSTS = [h.strip() for h in os.environ["DJANGO_ALLOWED_HOSTS"].split(",") if h.strip()]

SECURE_SSL_REDIRECT = os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "true").strip().lower() in {"1", "true", "yes", "y", "on"}
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = os.environ.get("DJANGO_USE_X_FORWARDED_HOST", "true").strip().lower() in {"1", "true", "yes", "y", "on"}
TRUST_X_FORWARDED_FOR = os.environ.get("DJANGO_TRUST_X_FORWARDED_FOR", "true").strip().lower() in {"1", "true", "yes", "y", "on"}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", "true").strip().lower() in {"1", "true", "yes", "y", "on"}
SECURE_HSTS_PRELOAD = os.environ.get("DJANGO_SECURE_HSTS_PRELOAD", "true").strip().lower() in {"1", "true", "yes", "y", "on"}
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = os.environ.get("DJANGO_SECURE_REFERRER_POLICY", "same-origin").strip()

CORS_ALLOW_CREDENTIALS = os.environ.get("DJANGO_CORS_ALLOW_CREDENTIALS", "false").strip().lower() in {"1", "true", "yes", "y", "on"}
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_ALL_ORIGINS = False

_allowed_origins_raw = os.environ.get("DJANGO_CORS_ALLOWED_ORIGINS", "").strip()
if _allowed_origins_raw:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _allowed_origins_raw.split(",") if o.strip()]
elif CORS_ALLOW_CREDENTIALS:
    raise RuntimeError("Missing required environment variable: DJANGO_CORS_ALLOWED_ORIGINS")

_csrf_trusted_origins_raw = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").strip()
if _csrf_trusted_origins_raw:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_trusted_origins_raw.split(",") if o.strip()]
