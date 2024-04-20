from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from dj_rest_auth.registration.views import (
    RegisterView,
    VerifyEmailView,
    ResendEmailVerificationView,
)
from .decorators import rate_limit


class LoginView(BaseLoginView):
    @rate_limit(action="signup")
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

