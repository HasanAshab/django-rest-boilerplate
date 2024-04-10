from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer as BaseAuthTokenSerializer
from api.common.serializers import ProtectedFieldSerializer
from .utils import send_verification_mail
from .models import User
from .tokens import verification_token


class RegisterSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'avatar')
        extra_kwargs = {'email': {'required': True, 'allow_blank': False}}
        
    def create(self, data):
        password = data.pop('password')
        user = User(**data)
        user.set_password(password)
        user.save()
        return user


class AuthTokenSerializer(BaseAuthTokenSerializer):
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data 

class SendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def save(self):
        email = self.validated_data['email']
        user = User.object.get(
            email=email,
            is_email_verified=False
        )
        if user:
            send_verification_mail(user)

class EmailVerificationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    token = serializers.CharField()
    
    def save(self):
        id = self.validated_data['id']
        token = self.validated_data['token']
        user = get_object_or_404(User, pk=id)
        verification_token.verify(user, token)
        user.is_email_verified = True
        return user.save()

class ListUserSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'links')

    def get_links(self, obj):
        return {
            'avatar': obj.avatar.url if obj.avatar else None,
            'profile': reverse('user-detail', kwargs={'username': obj.username}),
        }
    
    
class ProfileSerializer(serializers.ModelSerializer, ProtectedFieldSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')
        read_only_fields = ('date_joined', 'last_login', 'is_email_verified', 'is_active', 'is_superuser', 'is_staff', 'phone_number')
        extra_kwargs = {'avatar': {'read_only': False, 'write_only': True}}
        protected_fields = ('email', 'is_email_verified', 'phone_number', 'last_login')
        
    
    def should_show_protected_fields(self):
        return self.instance == self.context.get('user')
        
    def get_links(self, obj):
        return {
            'avatar': obj.avatar.url if obj.avatar else None,
        }

    def update(self, user, data):
        if 'email' in data and data['email'] != user.email:
            user.is_email_verified = False
        return super().update(user, data)
