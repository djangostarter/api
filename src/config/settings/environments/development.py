import os


DEBUG = True

# 开发环境默认只允许本机访问，避免无意间暴露到局域网/公网时被滥用。
_allowed_hosts_raw = os.environ.get("DJANGO_ALLOWED_HOSTS", "").strip()
if _allowed_hosts_raw:
    ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts_raw.split(",") if h.strip()]
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "testserver"]

# CORS：开发环境默认放开，便于本地前端调试；可通过环境变量收紧。
_cors_allow_all_raw = os.environ.get("DJANGO_CORS_ALLOW_ALL_ORIGINS", "true").strip().lower()
CORS_ALLOW_ALL_ORIGINS = _cors_allow_all_raw in {"1", "true", "yes", "y", "on"}
CORS_ORIGIN_ALLOW_ALL = CORS_ALLOW_ALL_ORIGINS

_cors_allow_credentials_raw = os.environ.get("DJANGO_CORS_ALLOW_CREDENTIALS", "false").strip().lower()
CORS_ALLOW_CREDENTIALS = _cors_allow_credentials_raw in {"1", "true", "yes", "y", "on"}

_allowed_origins_raw = os.environ.get("DJANGO_CORS_ALLOWED_ORIGINS", "").strip()
if _allowed_origins_raw:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _allowed_origins_raw.split(",") if o.strip()]
