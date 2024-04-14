from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, UpdateDestroyAPIView, RetrieveUpdateDestroyAPIView
from dj_rest_auth.views import (
    UserDetailsView as ProfileView,
    PasswordChangeView as DefaultPasswordChangeView
)
from .models import User
from .pagination import UserCursorPagination
from .serializers import ListUserSerializer, UserDetailsSerializer


class UsersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    pagination_class = UserCursorPagination
    
   
class ProfileView(ProfileView):
    def _check_role_change_permissions():
        data = self.request.data
        user = self.get_object()
        if 'is_staff' in data:
            user.assert_can('change_role_of_staff', user)
        if 'is_superuser' in data:
            user.assert_can('change_role_of_superuser', user)
        
    def _change_email(self, new_email):
        user = self.request.user
        user.email = new_email
        email_address = EmailAddress.objects.get_primary(user)
        email_address.email = new_email
        email_address.verified = False
        return email_address.save()

    def _send_confirmation(self, email_address):
        request = self.context.get('request')
        if request:
            email_address.send_confirmation(request, signup=False)

    def perform_update(self, serializer):
        self._check_role_change_permissions()

        new_email = self.request.data.pop('email', None)
        user = self.get_object()
        if new_email and new_email != user.email:
            email_address = self._change_email(new_email)
        serializer.save()
        
        if email_address:
            self._send_confirmation(email_address)

 
    
class UserDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserDetailsSerializer
    
    def perform_destroy(self, instance):
        self.request.user.assert_can('delete', instance)

    def perform_update(self, serializer):
        data = self.request.data
        user = self.get_object()
        if 'is_staff' in data:
            self.request.user.assert_can('change_role_of_staff', user)
        if 'is_superuser' in data:
            self.request.user.assert_can('change_role_of_superuser', user)
        serializer.save()


class PasswordChangeView(DefaultPasswordChangeView):
    http_method_names = ('patch',)
    
    def patch(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class PhoneNumberView(UpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PhoneNumberSerializer
    
    def get_object(self):
        return self.request.user