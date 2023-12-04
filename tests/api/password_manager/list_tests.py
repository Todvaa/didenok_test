import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from tests.factories import UserFactory, PasswordManagerFactory
from tests.utils import client


class PasswordManagerListTests(APITestCase):
    @pytest.mark.django_db
    def test_default(self):
        user = UserFactory()
        client.force_authenticate(user=user)
        PasswordManagerFactory.create_batch(10, user=user)
        response = client.get('/api/password/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    @pytest.mark.django_db
    def test_search(self):
        user = UserFactory()
        client.force_authenticate(user=user)
        PasswordManagerFactory(service_name='Test_1',user=user)
        PasswordManagerFactory(service_name='Test_10',user=user)
        PasswordManagerFactory(service_name='Test_2', user=user)
        PasswordManagerFactory(service_name='Test_20', user=user)
        response = client.get('/api/password/?service_name=Test_1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @pytest.mark.django_db
    def test_not_found(self):
        user = UserFactory()
        client.force_authenticate(user=user)
        PasswordManagerFactory(service_name='Test_1', user=user)
        PasswordManagerFactory(service_name='Test_10', user=user)
        PasswordManagerFactory(service_name='Test_2', user=user)
        PasswordManagerFactory(service_name='Test_20', user=user)
        response = client.get('/api/password/?service_name=easter_egg')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    @pytest.mark.django_db
    def test_foreign_schools(self):
        PasswordManagerFactory.create_batch(10)
        user = UserFactory()
        client.force_authenticate(user=user)
        response = client.get('/api/password/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
