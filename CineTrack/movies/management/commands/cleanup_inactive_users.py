from datetime import timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone


class Command(BaseCommand):

    help = 'Delete inactive users older than 24 hours'

    def handle(self, *args, **kwargs):

        expiry_time = timezone.now() - timedelta(hours=24)

        inactive_users = User.objects.filter(
            is_active=False,
            date_joined__lt=expiry_time
        )

        count = inactive_users.count()

        inactive_users.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully deleted {count} inactive user(s).'
            )
        )