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

    def test_retrieve_user_needs_authentication(
        self,
    ):
        user2 = UserFactory()
        url = reverse(
            "user-details",
            kwargs={"username": user2.username},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_retrieve_user(self):
        user2 = UserFactory()
        url = reverse(
            "user-details",
            kwargs={"username": user2.username},
        )
        data = UserDetailsSerializer(user2).data

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data, data)

    def test_can_not_be_staff(self):
        url = reverse(
            "user-details",
            kwargs={"username": self.user.username},
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"is_staff": True})

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(self.user.is_staff, False)

    def test_can_not_be_admin(self):
        url = reverse(
            "user-details",
            kwargs={"username": self.user.username},
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"is_superuser": True})

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            self.user.is_superuser,
            False,
        )

    def test_staff_can_be_user(self):
        staff = UserFactory(staff=True)
        url = reverse(
            "user-details",
            kwargs={"username": staff.username},
        )

        self.client.force_authenticate(user=staff)
        response = self.client.patch(url, {"is_staff": False})

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(staff.is_staff, False)

    def test_staff_can_not_be_admin(
        self,
    ):
        staff = UserFactory(staff=True)
        url = reverse(
            "user-details",
            kwargs={"username": staff.username},
        )

        self.client.force_authenticate(user=staff)
        response = self.client.patch(url, {"is_superuser": True})

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(staff.is_superuser, False)

    def test_admin_can_be_user(self):
        admin = UserFactory(admin=True)
        url = reverse(
            "user-details",
            kwargs={"username": admin.username},
        )

        self.client.force_authenticate(user=admin)
        response = self.client.patch(url, {"is_superuser": False})

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(admin.is_superuser, False)

    def test_admin_can_be_staff(self):
        admin = UserFactory(admin=True)
        url = reverse(
            "user-details",
            kwargs={"username": admin.username},
        )

        self.client.force_authenticate(user=admin)
        response = self.client.patch(url, {"is_staff": True})

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(admin.is_staff, True)
