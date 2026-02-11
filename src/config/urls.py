from django.contrib import admin
from django.urls import path

from api.v1 import api_v1


urlpatterns = [
    path("admin/", admin.site.urls),
    # 版本化 API 路由前缀：所有 API 都挂载在 /api/v1 下
    path("api/v1/", api_v1.urls),
]
