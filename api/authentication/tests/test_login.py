from django.urls import reverse
from rest_framework import status
from rest_framework.test import (
    APITestCase,
)
from api.accounts.models import User
from api.accounts.factories import (
    UserFactory,
)  # , LoggedDeviceFactory


class LoginTestCase(APITestCase):
    url = reverse("login")

    def setUp(self):
        self.user = UserFactory()

    def test_login_user(self):
        payload = {
            "username": self.user.username,
            "password": UserFactory.plain_password,
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertIn(
            "token",
            response.data["data"],
        )


def test_login_wrong_password(self):
    payload = {
        "email": self.user.email,
        "password": "wrong-pass",
    }

    response = self.client.post(self.url, payload)

    self.assertEqual(
        response.status_code,
        status.HTTP_401_UNAUTHORIZED,
    )
    self.assertNotIn("token", response.data)


def test_login_social_account(self):
    self.user = UserFactory(social=True)
    payload = {
        "email": self.user.email,
        "password": UserFactory.plain_password,
    }

    response = self.client.post(self.url, payload)

    self.assertEqual(
        response.status_code,
        status.HTTP_401_UNAUTHORIZED,
    )
    self.assertNotIn("token", response.data)


def test_prevent_brute_force_login(
    self,
):
    limit = 5
    responses = []
    payload = {
        "email": self.user.email,
        "password": "wrong-pass",
    }
    for _ in range(limit):
        response = self.client.post(
            reverse("auth:login"),
            payload,
        )
        responses.append(response)

    locked_response = self.client.post(reverse("auth:login"), payload)

    for response in responses:
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
    self.assertEqual(
        locked_response.status_code,
        status.HTTP_429_TOO_MANY_REQUESTS,
    )


def test_login_with_two_factor_auth(
    self,
):
    self.user = UserFactory(
        has_phone_number=True,
        two_factor_authenticable=True,
    )
    payload = {
        "email": self.user.email,
        "password": "password",
    }

    response = self.client.post(self.url, payload)

    self.assertEqual(
        response.status_code,
        status.HTTP_202_ACCEPTED,
    )
    self.assertNotIn("token", response.data)
    self.assertTrue(response.data.get("twoFactor", False))


def test_login_with_trusted_device(
    self,
):
    self.user = UserFactory(
        has_phone_number=True,
        two_factor_authenticable=True,
    )
    self.user = UserFactory().has_phone_number().two_factor_authenticable()
    device = LoggedDeviceFactory.create()
    self.user.trust_device(device, "127.0.0.1")
    payload = {
        "email": self.user.email,
        "password": "password",
    }

    response = self.client.post(
        self.url,
        payload,
        format="json",
        HTTP_X_DEVICE_ID=device.id,
    )

    self.assertEqual(
        response.status_code,
        status.HTTP_200_OK,
    )
    self.assertIn("token", response.data)
