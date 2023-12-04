import pytest
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from tests.factories import UserFactory
from tests.utils import client


def check_token(test: APITestCase, token: str):
    """Function to check JWT token validity."""

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    response = client.get('/api/auth/me/')
    test.assertEqual(response.status_code, status.HTTP_200_OK)
    client.credentials(HTTP_AUTHORIZATION=None)

    return response


class MeTests(APITestCase):
    """Test class for 'auth/me/' endpoint functionality"""
    @pytest.mark.django_db
    def test_valid(self):
        user = UserFactory()
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        response = check_token(self, token)
        self.assertEqual(user.username, response.data['username'])
