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
        fields = ('id', 'name', 'username', 'email', 'phone_number', 'avatar', 'is_superuser', 'is_staff', 'links')
        read_only_fields = ('is_superuser', 'is_staff', 'phone_number')
        extra_kwargs = {'avatar': {'read_only': False, 'write_only': True}}

    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if not request or not self.instance == request.user:
            self.remove_sensetive_fields()

    def remove_sensetive_fields(self):
        del self.fields['email']
        del self.fields['phone_number']
    
    def get_links(self, obj):
        return {
            'avatar': obj.avatar.url if obj.avatar else None,
        }


