from django.urls import reverse
from rest_framework import serializers
from api.common.utils import (
    twilio_verification,
)
from .models import User


class ProfileSerializer(serializers.ModelSerializer):
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
        )
        read_only_fields = (
            "date_joined",
            "last_login",
            "email",
            "is_email_verified",
            "is_active",
            "is_staff",
            "is_superuser",
            "phone_number",
        )


class LinkField(serializers.CharField):
    pass


class LinkMethodField(serializers.SerializerMethodField):
    def bind(self, field_name, parent):
        if self.method_name is None:
            self.method_name = f"get_{field_name}_link"

        super().bind(field_name, parent)


class LinksSerializerMixin:
    @property
    def _link_fields(self):
        return [
            field
            for field in self._readable_fields
            if isinstance(field, (LinkField, LinkMethodField))
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["links"] = {
            field.field_name: representation.pop(field.field_name)
            for field in self._link_fields
        }
        return representation


class ListUserSerializer(LinksSerializerMixin, serializers.ModelSerializer):
    self = LinkMethodField()
    avatar = LinkMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "self", "avatar")

    def get_self_link(self, user):
        return reverse("user-details", kwargs={"username": user.username})

    def get_avatar_link(self, user):
        return user.avatar.url if user.avatar else None


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "avatar",
            "date_joined",
            "is_superuser",
            "is_staff",
        )


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
