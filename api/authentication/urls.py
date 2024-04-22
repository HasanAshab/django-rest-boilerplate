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
from allauth.headless.mfa.views import (
    AuthenticateView,
    ReauthenticateView,
    AuthenticatorsView,
    ManageTOTPView,
    ManageRecoveryCodesView,
)


client = Client.APP



mfa_urlpatterns = [
    path(
        "authenticate/",
        AuthenticateView.as_api_view(client=client),
        name="authenticate",
    ),
    path(
        "reauthenticate/",
        ReauthenticateView.as_api_view(client=client),
        name="reauthenticate",
    ),
    path(
        "authenticators/",
        AuthenticatorsView.as_api_view(client=client),
        name="authenticators",
    ),
    path(
        "authenticators/totp/",
        ManageTOTPView.as_api_view(client=client),
        name="manage_totp",
    ),
    path(
        "authenticators/recovery-codes/",
        ManageRecoveryCodesView.as_api_view(client=client),
        name="manage_recovery_codes",
    ),
]


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
    path('two-factor/', include(mfa_urlpatterns))
]
