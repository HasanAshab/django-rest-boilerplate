from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .exceptions import InvalidTokenException


class TokenGenerator(PasswordResetTokenGenerator):
    def verify(self, user, token):
        if not self.check_token(user, token):
            raise InvalidTokenException


class VerificationTokenGenerator(TokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_email_verified}"


verification_token = VerificationTokenGenerator()
