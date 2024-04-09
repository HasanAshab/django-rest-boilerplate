from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.accounts import views


router = SimpleRouter()
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login')
]

