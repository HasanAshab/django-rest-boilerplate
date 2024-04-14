from django.urls import path, include
from .views import UsersView, ProfileView, UserDetailsView, PasswordChangeView, PhoneNumberChangeView


urlpatterns = [
  #  path('', include(router.urls)),
    path('', UsersView.as_view(), name='users'),
    path('me/', ProfileView.as_view(), name='profile'),
    path('me/password/', PasswordChangeView.as_view(), name='change-password'),
    #path('me/phone-number/', PhoneNumberChangeView.as_view(), name='change-password'),
    path('<str:username>/', UserDetailsView.as_view(), name='user-detail'),
]
