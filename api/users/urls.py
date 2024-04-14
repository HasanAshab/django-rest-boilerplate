from django.urls import path, include
from dj_rest_auth.views import UserDetailsView as ProfileView
from .views import UsersView, UserDetailsView, PasswordChangeView


urlpatterns = [
  #  path('', include(router.urls)),
    path('', UsersView.as_view(), name='users'),
    path('<str:username>', UserDetailsView.as_view(), name='user-detail'),
    path('me/', ProfileView.as_view(), name='profile'),
    path('me/password/', PasswordChangeView.as_view(), name='change-password'),
    #path('me/phone-number/', PasswordChangeView.as_view(), name='change-password'),
]
