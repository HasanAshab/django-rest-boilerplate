from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/auth/', include('api.auth.urls')),
    path('api/admin/', admin.site.urls),
    path('api/users/', include('api.users.urls')),
]