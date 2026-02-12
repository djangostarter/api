import os
from typing import Tuple


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "y", "on"}


_enable_account = _env_bool("DJANGO_STARTER_ENABLE_ACCOUNT_API", True)
_enable_billing = _env_bool("DJANGO_STARTER_ENABLE_BILLING_API", True)
_enable_demo = _env_bool("DJANGO_STARTER_ENABLE_DEMO_API", True)
_enable_integrations = _env_bool("DJANGO_STARTER_ENABLE_INTEGRATIONS_API", True)

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
    'apps.health.apps.HealthConfig',
)

if _enable_account:
    INSTALLED_APPS = INSTALLED_APPS + ('apps.account.apps.AccountConfig',)

if _enable_billing:
    INSTALLED_APPS = INSTALLED_APPS + ('apps.billing.apps.BillingConfig',)

if _enable_demo:
    INSTALLED_APPS = INSTALLED_APPS + ('apps.demo',)

if _enable_integrations:
    INSTALLED_APPS = INSTALLED_APPS + ('apps.integrations.apps.IntegrationsConfig',)
