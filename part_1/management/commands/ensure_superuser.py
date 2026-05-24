import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser from environment variables if one does not already exist."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.WARNING(
                    "Skipping superuser bootstrap because DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD is missing."
                )
            )
            return

        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD
        lookup = {username_field: username}

        if user_model.objects.filter(**lookup).exists():
            self.stdout.write(
                self.style.SUCCESS(f"Superuser '{username}' already exists.")
            )
            return

        user_model.objects.create_superuser(
            **{
                username_field: username,
                "email": email,
                "password": password,
            }
        )
        self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'."))
