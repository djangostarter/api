from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-starter-api-insecure-dev-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "ninja",
    "apps.health.apps.HealthConfig",
    "apps.authentication.apps.AuthenticationConfig",
    "apps.demo_crud",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DJANGO_DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DJANGO_DB_NAME", str(BASE_DIR / "db.sqlite3")),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = os.environ.get("DJANGO_LANGUAGE_CODE", "zh-hans")
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "Asia/Shanghai")
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = os.environ.get("DJANGO_CORS_ALLOW_ALL_ORIGINS", "1") == "1"

# django-starter-core 复用的 JWT 配置（保持与 DjangoStarter 生态一致）
# - 这里沿用了 settings.DJANGO_STARTER 的配置结构，以便直接复用核心库中的 JWT 生成/解析逻辑
# - 生产环境务必通过环境变量设置 DJANGO_JWT_SALT（不要提交到仓库）
DJANGO_STARTER = {
    "auth": {
        "jwt": {
            "algo": os.environ.get("DJANGO_JWT_ALGO", "HS256"),
            "salt": os.environ.get("DJANGO_JWT_SALT", "django-starter-api-insecure-jwt-salt"),
            "lifetime": int(os.environ.get("DJANGO_JWT_LIFETIME", "3600")),
        }
    }
}
