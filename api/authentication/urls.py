from django.urls import path, include
from allauth.headless.constants import Client
from allauth.headless.account.views import (
    SignupView,
    LoginView,
    ReauthenticateView,
    SessionView,
    VerifyEmailView,
    RequestPasswordResetView,
    ResetPasswordView,
)


client = Client.APP

from allauth.headless.mfa.urls import build_urlpatterns



urlpatterns = [
    path(
        "",
        include(build_urlpatterns(client))
    ), 
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
        "reauthenticate",
        ReauthenticateView.as_api_view(client=client),
        name="account_reauthenticate",
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
