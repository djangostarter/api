from django.urls import path
from ninja import NinjaAPI

from apps.account.apis.oauth2.weapp import router as weapp_router

api = NinjaAPI(urls_namespace="oauth2-weapp", version="0.0.0-test")
api.add_router("account/oauth2/weapp", weapp_router)

urlpatterns = [
    path("api/", api.urls),
]

