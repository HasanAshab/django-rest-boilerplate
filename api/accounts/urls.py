from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.common.utils import client_route
from api.accounts import views


router = SimpleRouter()
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/verification/', views.EmailVerificationView.as_view(), name='verification'),
    path('auth/verification/notification', views.SendEmailVerificationNotificationView.as_view(), name='send-verification')
    #path('auth/password/forgot', views.ForgotPasswordView.as_view(), name='forgot-password'),
    #path('auth/password/reset', views.ResetPasswordView.as_view(), name='reset-password')
]


client_route.add_paths({
  'email-verification': '/email/verify/{id}/{token}',
  'password-reset': '/password/reset/{id}/{token}',
})
