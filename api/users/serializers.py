from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import serializers


class ListUserSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'links']

    def get_links(self, obj):
        return {
            'avatar': None,
            'profile': reverse('user-detail', kwargs={'username': obj.username}),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    class Meta:
        model = User
        #fields = ['id', 'name', 'username', 'email', 'phone_number' 'is_superuser', 'is_stuff']
        fields = ['id', 'username', 'email', 'is_superuser', 'is_staff', 'links']
        
    def get_links(self, obj):
        return {
            'avatar': None,
        }


class ShowUserSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()
    class Meta:
        model = User
        #fields = ['id', 'name', 'username', 'is_superuser', 'is_stuff']
        fields = ['id', 'username', 'is_superuser', 'is_staff', 'links']
        
    def get_links(self, obj):
        return {
            'avatar': None,
        }