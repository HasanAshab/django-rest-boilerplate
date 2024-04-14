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
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from dj_rest_auth.views import PasswordChangeView as DefaultPasswordChangeView



class UsersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    pagination_class = UserCursorPagination
    
class UserDetailsView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserDetailsSerializer
    
    def perform_destroy(self, instance):
        self.request.user.assert_can('delete', instance)


class UserViewSet(ViewSet):
    lookup_field = 'username'
    permission_classes = (IsAuthenticated, IsEmailVerified)
    pagination_class = UserCursorPagination
    
    @action(detail=True, methods=[HTTPMethod.PATCH], url_path='admin')
    def make_admin(self, request, username):
        User.objects.filter(username=username).update(is_superuser=True)
        return Response({
            'message': 'Admin role granted to the user.'
        })
        
        
class PasswordChangeView(DefaultPasswordChangeView):
    http_method_names = ['patch']
    
    def patch(self, *args, **kwargs):
        return super().post(*args, **kwargs)
