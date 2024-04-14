from django.urls import reverse
from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer as DefaultProfileSerializer
from .models import User


class UserLinksSerializerMixin(metaclass=serializers.SerializerMetaclass):
    links = serializers.SerializerMethodField()
    
    def get_links(self, user):
        return {
            'avatar': user.avatar.url if user.avatar else None,
            **self.additional_links(user)
        }
    
    def additional_links(self, user):
        return {}


class ProfileSerializer(DefaultProfileSerializer, UserLinksSerializerMixin):
    
    class Meta(DefaultProfileSerializer.Meta):
        fields = ('id', 'email', 'is_email_verified', 'username', 'name', 'phone_number', 'avatar', 'date_joined', 'is_superuser', 'is_staff', 'links')
        read_only_fields = ('date_joined', 'last_login', 'is_email_verified', 'is_active', 'phone_number')
        extra_kwargs = {'avatar': {'read_only': False, 'write_only': True}}
    
class ListUserSerializer(serializers.ModelSerializer, UserLinksSerializerMixin):
    
    class Meta:
        model = User
        fields = ('id', 'username', 'links')

    def additional_links(self, obj):
        return {
            'profile': reverse('user-detail', kwargs={'username': obj.username}),
        }
 
class UserDetailsSerializer(serializers.ModelSerializer, UserLinksSerializerMixin):
    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'date_joined', 'is_superuser', 'is_staff', 'links')
        read_only_fields = ('username', 'name', 'date_joined')