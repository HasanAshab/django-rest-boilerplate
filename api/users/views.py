from http import HTTPMethod
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from api.authentication.permissions import IsEmailVerified
from .models import User
from .pagination import UserCursorPagination
from .serializers import ListUserSerializer, UserDetailsSerializer
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from dj_rest_auth.views import PasswordChangeView as DefaultPasswordChangeView



class UsersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    pagination_class = UserCursorPagination
    
class UserDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserDetailsSerializer
    
    def perform_destroy(self, instance):
        self.request.user.assert_can('delete', instance)
    
    def perform_update(self, instance):
        self.request.user.assert_can('change_role', instance)

class PasswordChangeView(DefaultPasswordChangeView):
    http_method_names = ['patch']
    
    def patch(self, *args, **kwargs):
        return super().post(*args, **kwargs)
