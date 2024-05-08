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
from drf_spectacular.utils import extend_schema
from api.docs.utils import successful_api_response
from .models import User
from .permissions import DeleteUserPermission
from .serializers import (
    ListUserSerializer,
    UserDetailsSerializer,
    ProfileSerializer,
    PhoneNumberSerializer,
)
from .pagination import UserPagination


class UsersView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = ListUserSerializer
    pagination_class = UserPagination


class ProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class UserDetailsView(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, DeleteUserPermission)
    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserDetailsSerializer


class PhoneNumberView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    def get_object(self):
        return self.request.user

    @extend_schema(
        request=PhoneNumberSerializer,
        responses={
            200: successful_api_response(),
            202: successful_api_response(
                description="Verification code sent to the phone number"
            ),
        },
    )
    def patch(self, request):
        serializer = PhoneNumberSerializer(
            self.get_object(),
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
