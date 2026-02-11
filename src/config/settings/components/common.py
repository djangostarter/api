import os

from config.settings import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-starter-api-insecure-dev-key")

# SECURITY WARNING: don't run with debug turned on in production!
# 读取环境变量判断是否开启Debug模式，无须手动设置
DEBUG = os.environ.get('DEBUG', 'true') == 'true'

# 读取环境变量判断是否docker环境，无须手动设置
DOCKER = os.environ.get('ENVIRONMENT', 'default') == 'docker'

URL_PREFIX = ""

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


