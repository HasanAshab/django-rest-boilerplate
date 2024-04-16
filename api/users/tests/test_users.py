from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.users.models import User 
from api.users.factories import UserFactory


class UsersTestCase(APITestCase):
    url = reverse('users')
    
    def setUp(self):
        self.user = UserFactory()
    
    def test_needs_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_users(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(self.url) 
        results = response.data['results']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.user.id)
