import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factories import PasswordManagerFactory, UserFactory
from tests.utils import client


class PasswordManagerDetailTests(APITestCase):
    @pytest.mark.django_db
    def test_default(self):
        password_manager = PasswordManagerFactory()
        client.force_authenticate(user=password_manager.user)
        response = client.get(
            f'/api/password/{password_manager.service_name}/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'service_name': password_manager.service_name,
            'password': password_manager.decrypted_password
        })

    @pytest.mark.django_db
    def test_not_found(self):
        user = UserFactory()
        password_manager = PasswordManagerFactory.build(user=user)
        response = client.get(
            f'/api/password/{password_manager.service_name}/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail': 'Not found.'})

    @pytest.mark.django_db
    def test_unauthenticated(self):
        password_manager = PasswordManagerFactory()
        client.force_authenticate(user=None)
        response = client.get(
            f'/api/password/{password_manager.service_name}/'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {
            'detail': 'Authentication credentials were not provided.'
        })

    @pytest.mark.django_db
    def test_no_permission(self):
        password_manager = PasswordManagerFactory()
        user = UserFactory()
        client.force_authenticate(user=user)
        response = client.get(
            f'/api/password/{password_manager.service_name}/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {
            'detail': 'Not found.'
        })
