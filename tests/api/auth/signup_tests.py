import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from password_manager.models import User
from tests.factories import UserFactory
from tests.utils import fake, client


class SignupTests(APITestCase):
    """Test class for Signin functionality."""

    @pytest.mark.django_db
    def test_valid(self):
        response = client.post('/api/auth/signup/', {
            'username': fake.name(),
            'password': fake.password()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(User.objects.count(), 1)

    @pytest.mark.django_db
    def test_existent_username(self):
        user = UserFactory()
        response = client.post('/api/auth/signup/', {
            'username': user.username,
            'password': fake.password(),
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'error': 'This username is already in use'
        })
