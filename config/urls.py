from django.contrib import admin
from django.urls import path, include
from api.accounts.models import User

print(list(User.objects.all())[1].email)

urlpatterns = [
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/admin/', admin.site.urls),
]