from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from api.users.models import User
from api.users.factories import (
    UserFactory,
)
from api.users.serializers import (
    ProfileSerializer,
)


class ProfileTestCase(APITestCase):
    url = reverse("profile")

    def setUp(self):
        self.user = UserFactory()

    def test_needs_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_show_profile(self):
        profile = ProfileSerializer(self.user).data

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data, profile)

    def test_update_email(self):
        new_email = "foo@gmail.com"

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.url,
            {"email": new_email},
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(self.user.email, new_email)
        self.assertEqual(
            self.user.is_email_verified,
            False,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [new_email])

    def test_updating_with_same_email(
        self,
    ):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self.url,
            {"email": self.user.email},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            self.user.is_email_verified,
            True,
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_delete_account(
        self,
    ):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url)
        user_deleted = not User.objects.filter(pk=self.user.pk).exists()

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertTrue(user_deleted)
