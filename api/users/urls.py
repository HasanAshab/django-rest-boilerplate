from django.urls import path
from .views import (
    UsersView,
    ProfileView,
    UserDetailsView,
    PasswordChangeView,
    PhoneNumberView,
)


urlpatterns = [
    path(
        "",
        UsersView.as_view(),
        name="users",
    ),
    path(
        "me/",
        ProfileView.as_view(),
        name="profile",
    ),
    path(
        "me/password/",
        PasswordChangeView.as_view(),
        name="change-password",
    ),
    path(
        "me/phone-number/",
        PhoneNumberView.as_view(),
        name="change-password",
    ),
    path(
        "<str:username>/",
        UserDetailsView.as_view(),
        name="user-details",
    ),
]
