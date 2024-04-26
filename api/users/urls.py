from django.urls import path
from allauth.headless.constants import Client
from allauth.headless.account.views import ManageEmailView
from .views import (
    UsersView,
    ProfileView,
    UserDetailsView,
    PasswordChangeView,
    PhoneNumberView,
)


client = Client.APP

urlpatterns = [
    path(
        "users/",
        UsersView.as_view(),
        name="users",
    ),
    path(
        "users/me/",
        ProfileView.as_view(),
        name="profile",
    ),
    path(
        "users/me/email/",
        ManageEmailView.as_api_view(client=client),
        name="manage_email",
    ),
    path(
        "users/me/password/",
        PasswordChangeView.as_api_view(client=client),
        name="password",
    ),
    path(
        "users/me/phone-number/",
        PhoneNumberView.as_view(),
        name="phone-number",
    ),
    path(
        "users/<str:username>/",
        UserDetailsView.as_view(),
        name="user-details",
    ),
]
