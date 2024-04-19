from django.urls import path
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
from api.common.utils import (
    client_route,
)

from .decorators import rate_limit
from django.utils.decorators import method_decorator

class L(LoginView):
    @rate_limit(action="signup")
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

urlpatterns = [
    path(
        "login/",
        L.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "verification/",
        VerifyEmailView.as_view(),
        name="verification",
    ),
    path(
        "verification/notifications/",
        ResendEmailVerificationView.as_view(),
        name="resend-verification",
    ),
    path(
        "password/reset",
        PasswordResetView.as_view(),
        name="reset-password",
    ),
    path(
        "password/reset/confirm",
        PasswordResetConfirmView.as_view(),
        name="confirm-reset-password",
    ),
]

client_route.update_paths(
    {
        "confirm-email-verification": "/email/verify/{key}",
        "confirm-password-reset": "/password/reset/{key}",
    }
)

