from django.test import TestCase
from api.users.factories import UserFactory
from api.users.policies import UserPolicy


class UserPolicyTestCase(TestCase):
    policy = UserPolicy()

    def test_user_can_delete_own_account(self):
        user = UserFactory()
        result = self.policy.delete(user, user)
        self.assertTrue(result)

    def test_user_can_not_delete_other_users(self):
        user1, user2 = UserFactory.create_batch(2)
        result = self.policy.delete(user1, user2)
        self.assertFalse(result)

    def test_staff_can_delete_own_account(self):
        staff = UserFactory(staff=True)
        result = self.policy.delete(staff, staff)
        self.assertTrue(result)

    def test_staff_can_delete_user(self):
        staff = UserFactory(staff=True)
        user = UserFactory()
        result = self.policy.delete(staff, user)
        self.assertTrue(result)

    def test_staff_can_not_delete_other_staffs(self):
        staff1 = UserFactory(staff=True)
        staff2 = UserFactory(staff=True)
        result = self.policy.delete(staff1, staff2)
        self.assertFalse(result)

    def test_staff_can_not_delete_admin(self):
        staff = UserFactory(staff=True)
        admin = UserFactory(admin=True)
        result = self.policy.delete(staff, admin)
        self.assertFalse(result)

    def test_admin_can_delete_own_account(self):
        admin = UserFactory(admin=True)
        result = self.policy.delete(admin, admin)
        self.assertTrue(result)

    def test_admin_can_delete_user(self):
        admin = UserFactory(admin=True)
        user = UserFactory()
        result = self.policy.delete(admin, user)
        self.assertTrue(result)

    def test_admin_can_delete_staff(self):
        admin = UserFactory(admin=True)
        staff = UserFactory(staff=True)
        result = self.policy.delete(admin, staff)
        self.assertTrue(result)

    def test_admin_can_not_delete_other_admins(self):
        admin1 = UserFactory(admin=True)
        admin2 = UserFactory(admin=True)
        result = self.policy.delete(admin1, admin2)
        self.assertFalse(result)

    def test_user_can_not_be_staff(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, {"is_staff": True})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.user.is_staff, False)

    def test_user_can_not_be_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(self.url, {"is_superuser": True})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.user.is_superuser, False)

    def test_user_can_not_make_staff(self):
        user2 = UserFactory()
        url = reverse("user-details", kwargs={"username": user2.username})

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"is_staff": True})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user2.is_staff, False)

    def test_user_can_not_make_admin(self):
        user2 = UserFactory()
        url = reverse("user-details", kwargs={"username": user2.username})

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"is_superuser": True})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user2.is_superuser, False)

    def test_staff_can_be_user(self):
        staff = UserFactory(staff=True)

        self.client.force_authenticate(user=staff)
        response = self.client.patch(self.url, {"is_staff": False})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(staff.is_staff, False)

    def test_staff_can_not_be_admin(self):
        staff = UserFactory(staff=True)

        self.client.force_authenticate(user=staff)
        response = self.client.patch(self.url, {"is_superuser": True})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(staff.is_superuser, False)

    def test_staff_can_not_make_staff(self):
        user2 = UserFactory()
        url = reverse("user-details", kwargs={"username": user2.username})

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"is_staff": True})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user2.is_staff, False)

    def test_staff_can_not_make_staff_to_user(self):
        user2 = UserFactory()
        url = reverse("user-details", kwargs={"username": user2.username})

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"is_staff": True})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user2.is_staff, False)

    def test_staff_can_not_make_staff_to_user(self):
        user2 = UserFactory()
        url = reverse("user-details", kwargs={"username": user2.username})

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"is_staff": True})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user2.is_staff, False)

    def test_staff_can_not_make_admin(self):
        user2 = UserFactory()
        url = reverse("user-details", kwargs={"username": user2.username})

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"is_superuser": True})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user2.is_superuser, False)

    def test_admin_can_be_staff(self):
        admin = UserFactory(admin=True)

        self.client.force_authenticate(user=admin)
        response = self.client.patch(self.url, {"is_staff": True})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(admin.is_staff, True)

    def test_admin_can_be_user(self):
        admin = UserFactory(admin=True)

        self.client.force_authenticate(user=admin)
        response = self.client.patch(self.url, {"is_superuser": False})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(admin.is_superuser, False)

    def test_staff_can_not_make_staff(self):
        user2 = UserFactory()
        url = reverse("user-details", kwargs={"username": user2.username})

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"is_staff": True})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user2.is_staff, False)

    def test_staff_can_not_make_admin(self):
        user2 = UserFactory()
        url = reverse("user-details", kwargs={"username": user2.username})

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, {"is_superuser": True})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(user2.is_superuser, False)
