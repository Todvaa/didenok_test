import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from tests.api.auth.me_tests import check_token
from tests.factories import UserFactory
from tests.utils import client


class SigninTests(APITestCase):
    """Test class for Signin functionality."""

    @pytest.mark.django_db
    def test_valid(self):
        user = UserFactory()
        response = client.post('/api/auth/signin/', {
            'username': user.username,
            'password': 'password',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        token = response.data['access']
        check_token(self, token)

    @pytest.mark.django_db
    def test_invalid_password(self):
        user = UserFactory()
        response = client.post('/api/auth/signin/', {
            'username': user.username,
            'password': 'invalid',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'detail': 'User not found'})
