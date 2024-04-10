from http import HTTPMethod
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.urls import reverse
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from knox.views import LoginView as KnoxLoginView
from .models import User
from .pagination import UserCursorPagination
from .serializers import RegisterSerializer, AuthTokenSerializer, EmailVerificationSerializer, ListUserSerializer, ProfileSerializer
from .utils import send_verification_mail
from .tokens import verification_token


class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get_post_response_headers(self, user):
        profile_url = reverse('user-detail', kwargs={'username': user.get('username')})
        return { 'location': profile_url }

    def get_post_response_data(self, user):
        return {
            'message': 'Verification email sent!',
            'data': user
        }

    def get_post_response(self, user):
        return Response(
            status=status.HTTP_201_CREATED,
            data=self.get_post_response_data(user),
            headers=self.get_post_response_headers(user)
        )
        
    def post(self, request, format=None): 
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data
        return self.get_post_response(user)


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    
    def get_post_response(self, request, token, instance):
        data = self.get_post_response_data(request, token, instance)
        return Response({
            'message': 'Logged in successfully!',
            'data': { 'token': data }
        })
        
    def post(self, request, format=None): 
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user:
            raise AuthenticationFailed()
        login(request, user)
        return super().post(request, format)
   
    
class SendEmailVerificationNotificationView(APIView):
    def post(self, request):
        serializer = SendEmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        Response('Verification link sent to email!', status=status.HTTP_202_ACCEPTED)

class EmailVerificationView(APIView):
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Email verified successfully!')
  
class UserViewSet(ViewSet):
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)
    pagination_class = UserCursorPagination

    def list(self, request):
        queryset = User.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        data = ListUserSerializer(result_page, many=True).data
        return paginator.get_paginated_response(data)
    
    def retrieve(self, request, username):
        user = get_object_or_404(User, username=username)
        profile = ProfileSerializer(user, context={'user': request.user}).data
        return Response({'data': profile})
    
    def destroy(self, request, username):
        user = get_object_or_404(User, username=username)
        request.user.assert_can('delete', user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, url_path='me')
    def profile(self, request):
        profile = ProfileSerializer(request.user, context={'user': request.user}).data
        return Response({'data': profile})
    
    @profile.mapping.patch
    def updateProfile(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if not user.is_email_verified:
            send_verification_mail(user)
            return Response({
                'message': 'Verification email sent to new Email Address!'
            })
        
        return Response({
            'message': 'Profile updated!'
        })

    @action(detail=True, methods=[HTTPMethod.PATCH], url_path='admin')
    def makeAdmin(self, request, username):
        User.objects.filter(username=username).update(is_superuser=True)
        return Response({
            'message': 'Admin role granted to the user.'
        })