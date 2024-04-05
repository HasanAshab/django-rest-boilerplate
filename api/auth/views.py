from django.contrib.auth import login
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from .serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView


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
    
