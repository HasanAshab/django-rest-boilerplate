from allauth.account.adapter import DefaultAccountAdapter
from api.common.utils import client_route


class AccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        return client_route.reverse(
            "confirm-email-verification",
            {"key": emailconfirmation.key},
        )

    def get_reset_password_from_key_url(self, key):
        return client_route.reverse(
            "confirm-password-reset",
            {"key": key},
        )
