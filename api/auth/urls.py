from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import RegisterView, LoginView


#router = SimpleRouter()
#router.register('login', LoginView.as_view(), name='login')

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login')
]