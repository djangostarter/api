from django.apps import AppConfig


class DemoCrudConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.demo_crud'
    verbose_name = 'Demo CRUD'
