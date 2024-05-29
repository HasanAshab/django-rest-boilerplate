from rest_framework import serializers
from api.common.utils import (
    twilio_verification,
)
from api.users.models import User
from api.users.mixins import UserAvatarLinkSerializerMixin


class ProfileSerializer(
    UserAvatarLinkSerializerMixin,
    serializers.ModelSerializer,
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
            "is_active",
            "is_staff",
            "is_superuser",
            "phone_number",
            "total_xp",
            "rank",
        )
        extra_kwargs = {"avatar": {"write_only": True}}


class PhoneNumberSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(required=False)

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
