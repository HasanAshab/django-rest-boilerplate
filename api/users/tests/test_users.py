from unittest.mock import patch
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
    UserDetailsSerializer,
)


class UsersTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def _reverse_user_url(self, user: User) -> str:
        return reverse(
            "user-details",
            kwargs={"username": user.username},
        )

    def test_list_users_needs_authentication(
        self,
    ):
        url = reverse("users")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_list_users(self):
        url = reverse("users")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        results = response.data["results"]

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]["id"],
            self.user.id,
        )

    def test_retrieving_user_needs_authentication(
        self,
    ):
        user2 = UserFactory()
        url = self._reverse_user_url(user2)

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_retrieve_user(self):
        user2 = UserFactory()
        url = self._reverse_user_url(user2)
        data = UserDetailsSerializer(user2).data

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data, data)

    def test_deleting_user_needs_authentication(
        self,
    ):
        user2 = UserFactory()
        url = self._reverse_user_url(user2)

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    @patch("api.authentication.mixins.HasPolicy.assert_can")
    def test_delete_user(self, mocked_policy_checker_method):
        user2 = UserFactory()
        url = self._reverse_user_url(user2)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        user_deleted = not User.objects.filter(pk=user2.pk).exists()

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        mocked_policy_checker_method.assert_called_once()
        action, checked_user = (
            mocked_policy_checker_method._mock_call_args.args
        )
        self.assertEqual(action, "delete")
        self.assertEqual(checked_user.username, user2.username)
        self.assertTrue(user_deleted)
