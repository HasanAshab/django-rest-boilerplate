from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from allauth.account.models import EmailAddress
from dj_rest_auth.views import (
    UserDetailsView as ProfileView,
    PasswordChangeView as DefaultPasswordChangeView
)
from api.common.response import APIResponse
from .models import User
from .pagination import UserCursorPagination
from .serializers import ListUserSerializer, UserDetailsSerializer, PhoneNumberSerializer


class UsersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    pagination_class = UserCursorPagination
    
   
class ProfileView(ProfileView):
    def perform_update(self, serializer):
        self._check_role_change_permissions()
        self._perform_email_change()
        serializer.save()
    
    def _check_role_change_permissions(self):
        data = self.request.data
        user = self.get_object()
        if 'is_staff' in data:
            user.assert_can('change_role_of_staff', user)
        if 'is_superuser' in data:
            user.assert_can('change_role_of_superuser', user)
       
    def _perform_email_change(self):
        user = self.get_object()
        new_email = self.request.data.pop('email')
        if new_email and new_email != user.email:
            email_address = self._change_email(new_email, commit=False)
            email_address.send_confirmation(self.request, signup=False)

    def _change_email(self, new_email, commit=False):
        user = self.get_object()
        user.email = new_email
        if commit:
            user.save()
        email_address = EmailAddress.objects.get_primary(user)
        email_address.email = new_email
        email_address.verified = False
        email_address.save()
        return email_address



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



class PhoneNumberView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
    
    def patch(self, request):
        serializer = PhoneNumberSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if 'otp' in serializer.validated_data:
            return APIResponse('Phone number updated!') 
        return APIResponse('Verification code sent to the phone number!', status=status.HTTP_202_ACCEPTED)
        
    def delete(self, request):
        user = self.get_object()
        user.phone_number = None
        user.save()
        return APIResponse(status=status.HTTP_204_NO_CONTENT)