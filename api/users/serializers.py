from django.urls import reverse
from rest_framework import serializers
from api.common.utils import (
    twilio_verification,
)
from api.common.serializers import (
    WrapSerializerDataMixin,
)
from .models import User


class UserLinksSerializerMixin(metaclass=serializers.SerializerMetaclass):
    links = serializers.SerializerMethodField()

    def get_links(self, user):
        return {
            "avatar": (user.avatar.url if user.avatar else None),
            **self.additional_links(user),
        }

    def additional_links(self, user):
        return {}


class ProfileSerializer(
    serializers.ModelSerializer,
    UserLinksSerializerMixin,
    WrapSerializerDataMixin,
):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "is_email_verified",
            "username",
            "name",
            "phone_number",
            "avatar",
            "date_joined",
            "is_superuser",
            "is_staff",
            "links",
        )
        read_only_fields = (
            "date_joined",
            "last_login",
            "email",
            "is_email_verified",
            "is_active",
            "phone_number",
        )
        extra_kwargs = {
            "avatar": {
                "read_only": False,
                "write_only": True,
            }
        }
        exclude_wrap_fields = ("links",)


class ListUserSerializer(
    serializers.ModelSerializer,
    UserLinksSerializerMixin,
):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "links",
        )

    def additional_links(self, obj):
        profile_url = reverse(
            "user-details",
            kwargs={"username": obj.username},
        )
        return {"profile": profile_url}


class UserDetailsSerializer(
    UserLinksSerializerMixin,
    WrapSerializerDataMixin,
    serializers.ModelSerializer,
):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "date_joined",
            "is_superuser",
            "is_staff",
            "links",
        )
        read_only_fields = (
            "username",
            "name",
            "date_joined",
        )
        exclude_wrap_fields = ("links",)


class PhoneNumberSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(
        max_length=6,
        min_length=6,
        required=False,
    )

    class Meta:
        model = User
        fields = ("phone_number", "otp")
        extra_kwargs = {"phone_number": {"required": True}}

    def validate_phone_number(self, phone_number):
        if phone_number == self.instance.phone_number:
            msg = "Phone number can't be same as old one."
            raise serializers.ValidationError(msg)
        return phone_number

    def validate_otp(self, otp):
        phone_number = self.initial_data["phone_number"]
        if not twilio_verification.is_valid(phone_number, otp):
            raise serializers.ValidationError("Invalid OTP code.")
        return otp

    def update(self, instance, validated_data):
        phone_number = validated_data.get("phone_number")
        otp = validated_data.get("otp")
        if not otp:
            twilio_verification.send_through_sms(phone_number)
            return instance
        instance.phone_number = phone_number
        instance.save()
        return instance
