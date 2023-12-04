from random import choice, randint
from string import ascii_letters, digits

from factory import LazyAttribute, PostGenerationMethodCall, SubFactory
from factory.django import DjangoModelFactory

from password_manager.models import PasswordManager, User
from tests.utils import fake


# see https://factoryboy.readthedocs.io/en/stable/index.html


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = LazyAttribute(lambda _: fake.name())
    password = PostGenerationMethodCall('set_password', 'password')


class PasswordManagerFactory(DjangoModelFactory):
    class Meta:
        model = PasswordManager

    service_name = LazyAttribute(lambda _: ''.join(
        choice(ascii_letters) for _ in range(randint(1, 255))
    ))
    password = LazyAttribute(lambda _: ''.join(
        choice(ascii_letters + digits) for _ in range(randint(1, 255))
    ))

    user = SubFactory(UserFactory)
