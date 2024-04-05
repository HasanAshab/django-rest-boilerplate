from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.serializers import ModelSerializer, SerializerMethodField


class ListUserSerializer(ModelSerializer):
    links = SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'links')

    def get_links(self, obj):
        return {
            'avatar': None,
            'profile': reverse('user-detail', kwargs={'username': obj.username}),
        }


class ProfileSerializer(ModelSerializer):
    links = SerializerMethodField()
    class Meta:
        model = User
        #fields = ('id', 'name', 'username', 'email', 'phone_number' 'is_superuser', 'is_stuff')
        fields = ('id', 'username', 'email', 'is_superuser', 'is_staff', 'links')
     
    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if not request or not self.instance == request.user:
            self.remove_sensetive_fields()

    def get_links(self, obj):
        return {
            'avatar': None,
        }
        
    def remove_sensetive_fields(self):
        del self.fields['email']
        #del self.fields['phone_number']


class ShowUserSerializer(ModelSerializer):
    links = SerializerMethodField()
    class Meta:
        model = User
        #fields = ('id', 'name', 'username', 'is_superuser', 'is_stuff')
        fields = ('id', 'username', 'is_superuser', 'is_staff', 'links')
        
    def get_links(self, obj):
        return {
            'avatar': None,
        }