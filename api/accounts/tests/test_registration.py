from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.common.test_utils import catch_signal, fake_file
from api.accounts.models import User
from api.accounts.signals import registered
from api.accounts.views import RegisterView


class RegistrationTestCase(APITestCase):
    url = reverse('register')
    
    def test_register_user(self):
        payload = {
            'username': 'foobar123',
            'email': 'foo@gmail.com',
            'password': 'Password@1234',
        }
        
        with catch_signal(registered) as handler: 
            response = self.client.post(self.url, payload)
        user = User.objects.filter(username=payload['username'], email=payload['email']).first()
       
        handler.assert_called_once_with(
            signal=registered,
            sender=RegisterView,
            user=user, 
            method='internal'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(user)

    def test_register_existing_email(self):
        user = User.objects.create(username='existing_user', email='existing@example.com')
        payload = {
            'username': 'new_user',
            'email': user.email,
            'password': 'Password@1234',
        }
    
        response = self.client.post(self.url, payload)
    
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_register_existing_username(self):
        user = User.objects.create(username='existing_user', email='existing@example.com')
        payload = {
            'username': user.username,
            'email': 'new@example.com',
            'password': 'Password@1234',
        }
    
        response = self.client.post(self.url, payload)
    
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_register_user_with_avatar(self):
        with fake_file('image.png') as avatar:
            payload = {
                'username': 'foobar123',
                'email': 'foo@gmail.com',
                'password': 'Password@1234',
                'avatar': avatar
            }
            response = self.client.post(self.url, payload, format='multipart')
        user = User.objects.filter(username=payload['username'], email=payload['email']).first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.avatar)