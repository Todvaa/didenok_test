import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factories import PasswordManagerFactory, UserFactory
from tests.utils import client


class PasswordManagerCreateTests(APITestCase):
    """Tests for creating a PasswordManager entry."""

    @pytest.mark.django_db
    def test_valid(self):
        password_manager = PasswordManagerFactory.build()
        client.force_authenticate(user=UserFactory())
        response = client.post(
            f'/api/password/{password_manager.service_name}/', {
                'password': password_manager.password
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'service_name': password_manager.service_name,
            'password': password_manager.password
        })

    @pytest.mark.django_db
    def test_empty_password(self):
        password_manager = PasswordManagerFactory.build()
        client.force_authenticate(user=UserFactory())
        response = client.post(
            f'/api/password/{password_manager.service_name}/', {
                'password': ''
            })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {
            'password': ['This field may not be blank.']
        })

    @pytest.mark.django_db
    def test_unauthenticated(self):
        password_manager = PasswordManagerFactory.build()
        client.force_authenticate(user=None)
        response = client.post(
            f'/api/password/{password_manager.service_name}/', {
                'password': password_manager.password
            })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data,{
            'detail': 'Authentication credentials were not provided.'
        })
