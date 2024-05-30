from django.urls import reverse
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, inline_serializer
from .models import User
from .mixins import UserAvatarLinkSerializerMixin


class ListUserSerializer(
    UserAvatarLinkSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = User
        fields = ("id", "username", "links")

    @extend_schema_field(
        inline_serializer(
            name="ListUserLinks",
            fields={
                "self": serializers.URLField(),
                "avatar": serializers.URLField(allow_null=True),
            },
        )
    )
    def get_links(self, user):
        return {
            **super().get_links(user),
            "self": reverse(
                "user_details", kwargs={"username": user.username}
            ),
        }


class UserDetailsSerializer(
    UserAvatarLinkSerializerMixin, serializers.ModelSerializer
):
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
            "links",
        )
        extra_kwargs = {"avatar": {"write_only": True}}
