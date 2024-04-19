from django.urls import path
from .views import (
    UsersView,
    ProfileView,
    UserDetailsView,
    PasswordChangeView,
    PhoneNumberView,
)


from django.utils.decorators import method_decorator
from api.authentication.decorators import rate_limit

@method_decorator(rate_limit(action="change_password"), name="patch")
class P(PasswordChangeView):
    pass


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
        P.as_view(),
        name="password",
    ),
    path(
        "me/phone-number/",
        PhoneNumberView.as_view(),
        name="phone-number",
    ),
    path(
        "<str:username>/",
        UserDetailsView.as_view(),
        name="user-details",
    ),
]
