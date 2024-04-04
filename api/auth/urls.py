from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import LoginView


#router = SimpleRouter()
#router.register('login', LoginView.as_view(), name='login')

urlpatterns = [
    path('login', LoginView.as_view(), name='login')
]
