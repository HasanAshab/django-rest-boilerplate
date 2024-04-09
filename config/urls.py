from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/', include('api.accounts.urls')),
    path('api/admin/', admin.site.urls),
]