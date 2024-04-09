from django.core.management.base import BaseCommand, CommandError
from api.accounts.factories import UserFactory
from knox.views import LoginView

class R():
    def __init__(self, user):
        self.user = user

class Command(BaseCommand):
    help = "Create a user and obtain auth token for testing"

    def handle(self, *args, **options):
        user = UserFactory()
        token = LoginView(request=R(user)).create_token()
        self.stdout.write(
            self.style.SUCCESS(f'Token: {token[1]}')
        )