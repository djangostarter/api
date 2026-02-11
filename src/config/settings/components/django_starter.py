import os


class ProjectInfo(object):
    def __init__(self, name: str, description: str = ''):
        self.name = name
        self.description = description


project_info = ProjectInfo(
    os.environ.get("DJANGO_STARTER_PROJECT_NAME", "DjangoStarter API"),
    os.environ.get("DJANGO_STARTER_PROJECT_DESC", ""),
)

# DjangoStarter 框架配置
DJANGO_STARTER = {
    'project_info': {
        'name': project_info.name,
        'description': project_info.description,
    },
    'site': {
        # 控制是否开启网站留言联系功能
        'enable_contact_form': os.environ.get("DJANGO_STARTER_ENABLE_CONTACT_FORM", "false") == "true",
    },
    # 管理后台的配置
    'admin': {
        'site_header': project_info.name,
        'site_title': project_info.name,
        'index_title': project_info.name,
        'list_per_page': 20
    },
    # 认证配置
    'auth': {
        # JWT 配置
        'jwt': {
            # 算法
            'algo': os.environ.get("DJANGO_JWT_ALGO", "HS256"),
            # 随机的salt密钥，只有token生成者（同时也是校验者）自己能有，用于校验生成的token是否合法
            'salt': os.environ.get("DJANGO_JWT_SALT", "django-starter-api-insecure-jwt-salt"),
            # token 有效时间 （单位：秒）
            'lifetime': int(os.environ.get("DJANGO_JWT_LIFETIME", str(12 * 60 * 60))),
        }
    },
    # 第三方登录配置
    'oauth2': {
        # 微信登录配置
        'wechat': {
            'enabled': os.environ.get("DJANGO_OAUTH2_WECHAT_ENABLED", "false") == "true",
            'app_id': os.environ.get("DJANGO_OAUTH2_WECHAT_APP_ID", ""),
            'secret': os.environ.get("DJANGO_OAUTH2_WECHAT_SECRET", ""),
            'redirect_uri': os.environ.get("DJANGO_OAUTH2_WECHAT_REDIRECT_URI", ""),
        },
        # 企业微信配置
        'wecom': {
            'enabled': os.environ.get("DJANGO_OAUTH2_WECOM_ENABLED", "false") == "true",
            'corp_id': os.environ.get("DJANGO_OAUTH2_WECOM_CORP_ID", ""),
            'secret': os.environ.get("DJANGO_OAUTH2_WECOM_SECRET", ""),
            'redirect_uri': os.environ.get("DJANGO_OAUTH2_WECOM_REDIRECT_URI", ""),
        },
        # 微信小程序配置
        'weapp': {
            'enabled': os.environ.get("DJANGO_OAUTH2_WEAPP_ENABLED", "false") == "true",
            'appid': os.environ.get("DJANGO_OAUTH2_WEAPP_APPID", ""),
            'secret': os.environ.get("DJANGO_OAUTH2_WEAPP_SECRET", ""),
        }
    }
}
