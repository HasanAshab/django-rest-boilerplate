from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.common.utils import client_route
from api.accounts import views


router = SimpleRouter()
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login')
]


client_route.add_paths({
  'email-verification': '/email/verify/{id}/{token}',
  'password-reset': '/password/reset/{id}/{token}',
})
