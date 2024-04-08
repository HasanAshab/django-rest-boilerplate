from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.serializers import AuthTokenSerializer as BaseAuthTokenSerializer
from rest_framework.serializers import ModelSerializer
from api.users.models import User


class RegisterSerializer(ModelSerializer):
   
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
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs 