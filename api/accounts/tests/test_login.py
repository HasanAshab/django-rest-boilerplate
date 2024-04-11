from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myapp.models import User  # Assuming User is your Django user model
from myapp.factories import UserFactory, LoggedDeviceFactory  # Assuming you have factories for User and LoggedDevice

class AuthLoginTest(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()

    def test_login_user(self):
        url = reverse('auth:login')
        payload = {
            'email': self.user.email,
            'password': 'password',
        }

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_wrong_password(self):
        url = reverse('auth:login')
        payload = {
            'email': self.user.email,
            'password': 'wrong-pass',
        }

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('token', response.data)

    def test_login_social_account(self):
        self.user = UserFactory(social=True).create()
        url = reverse('auth:login')
        payload = {
            'email': self.user.email,
            'password': 'password',
        }

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('token', response.data)

    def test_prevent_brute_force_login(self):
        limit = 5
        responses = []
        payload = {
            'email': self.user.email,
            'password': 'wrong-pass',
        }

        for _ in range(limit):
            response = self.client.post(reverse('auth:login'), payload, format='json')
            responses.append(response)

        locked_response = self.client.post(reverse('auth:login'), payload, format='json')

        for response in responses:
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(locked_response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_login_with_two_factor_auth(self):
        self.user = UserFactory(has_phone_number=True, two_factor_authenticable=True).create()

        url = reverse('auth:login')
        payload = {
            'email': self.user.email,
            'password': 'password',
        }

        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertNotIn('token', response.data)
        self.assertTrue(response.data.get('twoFactor', False))

    def test_login_with_trusted_device(self):
        self.user = UserFactory(has_phone_number=True, two_factor_authenticable=True).create()
        self.user = UserFactory().has_phone_number().two_factor_authenticable().create()
        device = LoggedDeviceFactory.create()
        self.user.trust_device(device, '127.0.0.1')

        url = reverse('auth:login')
        payload = {
            'email': self.user.email,
            'password': 'password',
        }

        response = self.client.post(url, payload, format='json', HTTP_X_DEVICE_ID=device.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
