from django.core.management.base import BaseCommand

from apps.integrations.models import AppClient


class Command(BaseCommand):
    help = "List AppClients (without secrets)."

    def handle(self, *args, **options):
        for client in AppClient.objects.all().order_by("-id"):
            self.stdout.write(
                f"id={client.id} app_id={client.app_id} key_id={client.key_id} status={client.status} scopes={client.scopes} allowed_ips={client.allowed_ips}"
            )

