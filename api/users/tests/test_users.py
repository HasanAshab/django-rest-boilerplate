from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.users.models import User 
from api.users.factories import UserFactory
from api.users.serializers import UserDetailsSerializer


class UsersTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
    
    def test_list_users_needs_authentication(self):
        url = reverse('users')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_users(self):
        url = reverse('users')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url) 
        results = response.data['results']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['id'], self.user.id)
    
    def test_retrieve_user_needs_authentication(self):
        user2 = UserFactory()
        url = reverse('user-details', kwargs={'username': user2.username})
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_user(self):
        user2 = UserFactory()
        url = reverse('user-details', kwargs={'username': user2.username})
        data = UserDetailsSerializer(user2).data
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url) 
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)
    
    def test_can_delete_own_account(self):
        url = reverse('user-details', kwargs={'username': self.user.username})

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url) 

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
    
    def test_can_not_delete_other_users(self):
        user2 = UserFactory()
        url = reverse('user-details', kwargs={'username': user2.username})
       
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url) 

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(pk=user2.pk).exists())
    
    def test_staff_can_delete_own_account(self):
        staff = UserFactory(staff=True)
        url = reverse('user-details', kwargs={'username': staff.username})
       
        self.client.force_authenticate(user=staff)
        response = self.client.delete(url) 

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=staff.pk).exists())
    
    def test_staff_can_delete_user(self):
        staff = UserFactory(staff=True)
        user = UserFactory()
        url = reverse('user-details', kwargs={'username': user.username})
       
        self.client.force_authenticate(user=staff)
        response = self.client.delete(url) 

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=user.pk).exists())
    
    def test_staff_can_not_delete_other_staffs(self):
        staff, staff2 = UserFactory.create_batch(2, staff=True)
        url = reverse('user-details', kwargs={'username': staff2.username})
       
        self.client.force_authenticate(user=staff)
        response = self.client.delete(url) 

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(pk=staff2.pk).exists())
    
    def test_staff_can_not_delete_admin(self):
        staff = UserFactory(staff=True)
        admin = UserFactory(admin=True)
        url = reverse('user-details', kwargs={'username': admin.username})
        
        self.client.force_authenticate(user=staff)
        response = self.client.delete(url) 

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(pk=admin.pk).exists())
    
    def test_admin_can_delete_own_account(self):
        admin = UserFactory(admin=True)
        url = reverse('user-details', kwargs={'username': admin.username})
       
        self.client.force_authenticate(user=admin)
        response = self.client.delete(url) 

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=admin.pk).exists())
    
    def test_admin_can_delete_user(self):
        admin = UserFactory(admin=True)
        user = UserFactory()
        url = reverse('user-details', kwargs={'username': user.username})
       
        self.client.force_authenticate(user=admin)
        response = self.client.delete(url) 

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=user.pk).exists())
    
    def test_admin_can_delete_staff(self):
        admin = UserFactory(admin=True)
        staff = UserFactory(staff=True)
        url = reverse('user-details', kwargs={'username': staff.username})
       
        self.client.force_authenticate(user=admin)
        response = self.client.delete(url) 

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=staff.pk).exists())

    def test_admin_can_not_delete_other_admins(self):
        admin, admin2 = UserFactory.create_batch(2, admin=True)
        url = reverse('user-details', kwargs={'username': admin2.username})
        
        self.client.force_authenticate(user=admin)
        response = self.client.delete(url) 

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(pk=admin2.pk).exists())