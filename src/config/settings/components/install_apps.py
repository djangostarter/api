from typing import Tuple

# 应用定义
INSTALLED_APPS: Tuple[str, ...] = (
    # 后台扩展
    "jazzmin",
    # 'multi_captcha_admin',

    # Django核心
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # DjangoStarter组件
    'django_starter_core.contrib.about',
    'django_starter_core.contrib.admin',
    'django_starter_core.contrib.auth',
    'django_starter_core.contrib.code_generator',
    'django_starter_core.contrib.config',
    'django_starter_core.contrib.docs',
    'django_starter_core.contrib.guide',
    'django_starter_core.contrib.navbar',
    'django_starter_core.contrib.notifications',
    'django_starter_core.contrib.seed',

    # 第三方组件
    'captcha',
    'corsheaders',
    'django_watchfiles',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    'simple_history',

    # 我们自己的应用
    'apps.account.apps.AccountConfig',
    'apps.billing.apps.BillingConfig',
    'apps.demo',
    'apps.health.apps.HealthConfig',
)
