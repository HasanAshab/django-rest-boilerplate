from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from drf_standardized_response.openapi.utils import standard_openapi_response
from .serializers import (
    ProfileSerializer,
    PhoneNumberSerializer,
)


class ProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class PhoneNumberView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = None

    @extend_schema(
        request=PhoneNumberSerializer,
        responses={
            200: standard_openapi_response(),
            202: standard_openapi_response(
                description="Verification code sent to the phone number"
            ),
        },
    )
    def patch(self, request):
        serializer = PhoneNumberSerializer(
            self.request.user,
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
        user = self.request.user
        user.phone_number = ""
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
