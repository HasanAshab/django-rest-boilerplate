from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.users"

    def ready(self):
        from .models import User

        u1 = User.objects.first()
        u2 = User.objects.first()

        print(
            u1.__dict__,
            "\n\n",
            u2.__dict__,
        )
