from rest_framework import serializers
from allauth.account.models import EmailAddress
from dj_rest_auth.serializers import (
    PasswordResetSerializer as DefaultPasswordResetSerializer,
    UserDetailsSerializer as DefaultUserDetailsSerializer,
)
from api.common.utils import client_route


def password_reset_url_generator(request, user, temp_key):
    return client_route.reverse('confirm-password-reset', {'key': temp_key})

class PasswordResetSerializer(DefaultPasswordResetSerializer):
    def get_email_options(self):
        return {'url_generator': password_reset_url_generator}
        
        
class UserDetailsSerializer(DefaultUserDetailsSerializer):
    is_email_verified = serializers.SerializerMethodField()
 
    def get_is_email_verified(self, user):    
        return user.emailaddress_set.filter(primary=True, verified=True).exists()

    class Meta(DefaultUserDetailsSerializer.Meta):
        fields = DefaultUserDetailsSerializer.Meta.fields + ('is_email_verified',)
        read_only_fields = []
    
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