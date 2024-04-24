from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView,
)
from allauth.headless.account.views import ChangePasswordView
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


class ProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user
    
class UserDetailsView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserDetailsSerializer

    def perform_destroy(self, instance):
        self.request.user.assert_can("delete", instance)
        super().perform_destroy(instance)


class PasswordChangeView(ChangePasswordView):
    http_method_names = ("patch",)

    def patch(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class PhoneNumberView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None
    
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
            return Response("Phone number updated!")
        return Response(
            "Verification code sent to the phone number!",
            status=status.HTTP_202_ACCEPTED,
        )

    def delete(self, request):
        user = self.get_object()
        user.phone_number = None
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
