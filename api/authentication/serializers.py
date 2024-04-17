from dj_rest_auth.serializers import (
    PasswordResetSerializer as DefaultPasswordResetSerializer,
)
from api.common.utils import client_route


def password_reset_url_generator(request, user, temp_key):
    return client_route.reverse("confirm-password-reset", {"key": temp_key})


class PasswordResetSerializer(DefaultPasswordResetSerializer):
    def get_email_options(self):
        return {"url_generator": password_reset_url_generator}
