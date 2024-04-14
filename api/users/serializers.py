from django.urls import reverse
from rest_framework import serializers
from allauth.account.models import EmailAddress
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
    
    def _change_email(self, user, new_email):
        user.email = new_email
        user.save()
        email_address = EmailAddress.objects.get_primary(user)
        email_address.email = new_email
        email_address.verified = False
        return email_address.save()

    def _send_confirmation(self, email_address):
        request = self.context.get('request')
        if request:
            email_address.send_confirmation(request, signup=False)

    def update(self, instance, validated_data):
        new_email = validated_data.pop('email', None)
        user = super().update(instance, validated_data)
        if new_email and new_email != user.email:
            email_address = self._change_email(user, new_email)
            self._send_confirmation(email_address)
        return user

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