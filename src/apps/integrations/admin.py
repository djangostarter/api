from django.contrib import admin

from .models import AppClient


@admin.register(AppClient)
class AppClientAdmin(admin.ModelAdmin):
    list_display = ("id", "app_id", "app_name", "key_id", "status", "created_time", "updated_time")
    list_filter = ("status", "created_time")
    search_fields = ("app_id", "app_name", "key_id")
    readonly_fields = ("guid", "key_id", "secret_hash", "created_time", "updated_time")

