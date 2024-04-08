from django.urls import reverse
from rest_framework import serializers
from .models import User


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


class ProfileSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions')
        read_only_fields = ('date_joined', 'last_login', 'is_email_verified', 'is_active', 'is_superuser', 'is_staff', 'phone_number')
        extra_kwargs = {'avatar': {'read_only': False, 'write_only': True}}

    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        user = self.context.get('user')
        if not self.instance != user:
            self.remove_sensetive_fields()

    def remove_sensetive_fields(self):
        del self.fields['email']
        del self.fields['is_email_verified']
        del self.fields['phone_number']
        del self.fields['last_login']
    
    def get_links(self, obj):
        return {
            'avatar': obj.avatar.url if obj.avatar else None,
        }

    def update(self, user, data):
        if 'email' in data and data['email'] != user.email:
            user.is_email_verified = False
        return super().update(user, data)
