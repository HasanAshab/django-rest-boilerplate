from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


urlpatterns = [
    path(
        "api/",
        include("allauth.account.urls"),
    ),
    path("api/admin/", admin.site.urls),
    path(
        "api/auth/",
        include("api.authentication.urls"),
    ),
    path(
        "api/users/",
        include("api.users.urls"),
    ),
]


def handler404(request, exception=None):
    return JsonResponse(
        {"message": "Page not found"},
        status=404,
    )
