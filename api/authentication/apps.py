from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.authentication"

    def ready(self):
        self._register_client_urls()

    def _register_client_urls(self):
        from api.common.utils import client_route

        client_route.update_paths(
            {
                "confirm-email-verification": "/email/verify/{key}",
                "confirm-password-reset": "/password/reset/{key}",
            }
        )
