from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.users.models import User 
from api.users.factories import UserFactory
from api.users.serializers import ProfileSerializer


class ProfileTestCase(APITestCase):
    url = reverse('profile')
    
    def setUp(self):
        self.user = UserFactory()
    
    def test_needs_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile(self):
        self.client.force_authenticate(user=self.user)
        profile = ProfileSerializer(self.user).data

        response = self.client.get(self.url) 
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, profile)