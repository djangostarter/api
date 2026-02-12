# Cors Header 配置
import os

from config.settings.components.common import DEBUG


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


CORS_ALLOW_CREDENTIALS = _env_bool("DJANGO_CORS_ALLOW_CREDENTIALS", False)
CORS_ORIGIN_ALLOW_ALL = _env_bool("DJANGO_CORS_ALLOW_ALL_ORIGINS", DEBUG)
CORS_ALLOW_ALL_ORIGINS = CORS_ORIGIN_ALLOW_ALL

_allowed_origins_raw = os.environ.get("DJANGO_CORS_ALLOWED_ORIGINS", "").strip()
if _allowed_origins_raw:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _allowed_origins_raw.split(",") if o.strip()]
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# 其他跨域配置
XS_SHARING_ALLOWED_METHODS = ['POST', 'GET', 'OPTIONS', 'PUT', 'DELETE']
