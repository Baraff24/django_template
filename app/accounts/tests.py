from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .constants import PENDING_COMPLETE_DATA, COMPLETE
from .models import User


class UserTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client = APIClient()

    def test_users_list_api(self):
        # Ensure that the UsersListAPI view returns
        # a 200 status code when accessed by a superuser
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_api(self):
        # Ensure that the UserDetailAPI view returns
        # a 200 status code when accessed by a superuser
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complete_profile_api(self):
        # Ensure that the CompleteProfileAPI view updates the user's profile correctly
        self.user.status = PENDING_COMPLETE_DATA
        self.user.save()
        self.client.force_authenticate(user=self.user)
        url = reverse('complete-profile')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'telephone': '1234567890',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.telephone, '1234567890')
        self.assertEqual(self.user.status, COMPLETE)

    def test_complete_profile_api_already_completed(self):
        # Ensure that the CompleteProfileAPI view returns
        # a 400 status code if the profile is already completed
        self.user.status = COMPLETE
        self.user.save()
        self.client.force_authenticate(user=self.user)
        url = reverse('complete-profile')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'telephone': '1234567890',
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_user(self):
        # Ensure that an inactive user cannot access protected views
        self.user.is_active = False
        self.user.save()
        self.client.force_authenticate(user=self.user)
        url = reverse('users-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserModelTests(TestCase):
    def test_user_model_str(self):
        # Ensure that the User model's __str__ method returns the expected string
        user = User(username='testuser', email='test@example.com')
        self.assertEqual(str(user), 'testuser - test@example.com')
