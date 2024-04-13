from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account import app_settings
from api.common.utils import client_route


class AccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        return client_route.reverse('confirm-email-verification', {'key': emailconfirmation.key})