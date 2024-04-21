from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from allauth.account.models import (
    EmailAddress,
)
from allauth.headless.account.views import ChangePasswordView
from api.common.response import (
    APIResponse,
)
from .models import User
from .serializers import (
    ListUserSerializer,
    UserDetailsSerializer,
    ProfileSerializer,
    PhoneNumberSerializer,
)
from .pagination import UserCursorPagination


class UsersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    pagination_class = UserCursorPagination

from allauth.headless.base.views import AuthenticatedAPIView



class ProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        #self._check_role_change_permissions()
        serializer.save()

    def _check_role_change_permissions(
        self,
    ):
        data = self.request.data
        user = self.get_object()
        is_staff = data.get('is_staff')
        is_superuser = data.get('is_superuser') 
        
        if is_superuser is True:
            role = 'admin'
        elif is_staff is True:
            role = 'staff'
        elif is_superuser is False and is_staff is False:
            role = 'general_user'
        
        if role:
            user.assert_can(f'make_{role}', user)
        
        # if "is_staff" in data:
    
    def _check_role_change_permissions(
        self,
    ):
        user = self.get_object()
        role = self.request.data.get('role')
        if role:
            user.assert_can(f'make_{role}', user)
        
        # if "is_staff" in data:


class UserDetailsView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserDetailsSerializer

    def perform_destroy(self, instance):
        self.request.user.assert_can("delete", instance)
        instance.delete()

    def perform_update(self, serializer):
        data = self.request.data
        user = self.get_object()
        if "is_staff" in data:
            self.request.user.assert_can(
                "change_staff_role",
                user,
            )
        if "is_superuser" in data:
            self.request.user.assert_can(
                "change_role_of_superuser",
                user,
            )
        serializer.save()


class PasswordChangeView(ChangePasswordView):
    http_method_names = ("patch",)

    def patch(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class PhoneNumberView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def patch(self, request):
        serializer = PhoneNumberSerializer(
            request.user,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if "otp" in serializer.validated_data:
            return APIResponse("Phone number updated!")
        return APIResponse(
            "Verification code sent to the phone number!",
            status=status.HTTP_202_ACCEPTED,
        )

    def delete(self, request):
        user = self.get_object()
        user.phone_number = None
        user.save()
        return APIResponse(status=status.HTTP_204_NO_CONTENT)
