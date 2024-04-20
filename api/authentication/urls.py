from django.urls import path
from allauth.headless.constants import Client
from allauth.headless.account.views import (
    SignupView,
    LoginView,
    SessionView,
    VerifyEmailView,
    RequestPasswordResetView,
    ResetPasswordView,
    ManageEmailView
)
from api.common.utils import \
    client_route


client = Client.APP

urlpatterns = [
    path(
        "signup",
        SignupView.as_api_view(client=client),
        name="signup",
    ),
    path(
        "login",
        LoginView.as_api_view(client=client),
        name="login",
    ),
    path(
        "session",
        SessionView.as_api_view(client=client),
        name="current-session",
    ),
    path(
        "email/verify",
        VerifyEmailView.as_api_view(client=client),
        name="verify-email",
    ),
    path(
        "password/reset/request",
        RequestPasswordResetView.as_api_view(client=client),
        name="request-reset-password",
    ),
    path(
        "password/reset/confirm",
        ResetPasswordView.as_api_view(client=client),
        name="confirm-reset-password",
    ),
]

client_route.update_paths(
    {
        "confirm-email-verification": "/email/verify/{key}",
        "confirm-password-reset": "/password/reset/{key}",
    }
)