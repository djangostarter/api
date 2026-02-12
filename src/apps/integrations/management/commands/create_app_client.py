import secrets
import uuid

from django.core.management.base import BaseCommand, CommandParser

from apps.integrations.models import AppClient, AppClientStatus


class Command(BaseCommand):
    help = "Create an AppClient and print its API key once."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--app-id", required=True)
        parser.add_argument("--app-name", required=True)
        parser.add_argument("--allowed-ips", default="")
        parser.add_argument("--scopes", default="")
        parser.add_argument("--inactive", action="store_true")

    def handle(self, *args, **options):
        app_id: str = options["app_id"]
        app_name: str = options["app_name"]
        allowed_ips: str = options["allowed_ips"] or ""
        scopes: str = options["scopes"] or ""
        inactive: bool = bool(options["inactive"])

        key_id = uuid.uuid4().hex
        secret = secrets.token_urlsafe(32)

        client = AppClient(
            app_id=app_id,
            app_name=app_name,
            key_id=key_id,
            allowed_ips=allowed_ips,
            scopes=scopes,
            status=AppClientStatus.INACTIVE if inactive else AppClientStatus.ACTIVE,
        )
        client.set_secret(secret)
        client.save()

        self.stdout.write(self.style.SUCCESS("AppClient created"))
        self.stdout.write(f"app_id: {client.app_id}")
        self.stdout.write(f"key_id: {client.key_id}")
        self.stdout.write("API key (print once):")
        self.stdout.write(f"{client.key_id}.{secret}")

