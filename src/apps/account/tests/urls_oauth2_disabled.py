from django.urls import path
from ninja import NinjaAPI

api = NinjaAPI(urls_namespace="oauth2-disabled", version="0.0.0-test")

urlpatterns = [
    path("api/", api.urls),
]

