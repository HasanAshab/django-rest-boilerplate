from django.contrib.auth import login
from django.urls import reverse
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from knox.views import LoginView as KnoxLoginView
from .serializers import RegisterSerializer, AuthTokenSerializer


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
    

