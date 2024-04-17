from allauth.account.adapter import (
    DefaultAccountAdapter,
)
from api.common.utils import (
    client_route,
)


class AccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        return client_route.reverse(
            "confirm-email-verification",
            {"key": emailconfirmation.key},
        )
