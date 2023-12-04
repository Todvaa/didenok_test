from collections import OrderedDict

from rest_framework.serializers import (
    ModelSerializer, Serializer, CharField
)
from rest_framework.validators import UniqueTogetherValidator

from password_manager.models import PasswordManager


class AuthSerializer(Serializer):
    username = CharField(max_length=255, required=True)
    password = CharField(
        max_length=150, write_only=True, required=True
    )


class PasswordManagerSerializer(ModelSerializer):
    password = CharField(max_length=255, required=True)
    service_name = CharField(max_length=255, required=True)

    class Meta:
        model = PasswordManager
        fields = ('service_name', 'password', )
        validators = [
            UniqueTogetherValidator(
                queryset=PasswordManager.objects.all(),
                fields=('service_name', 'password', )
            )
        ]

    def to_representation(self, instance):
        if isinstance(instance, PasswordManager):
            instance = OrderedDict(
                {
                    'service_name': instance.service_name,
                    'password': instance.decrypted_password
                }
            )
        representation = super().to_representation(instance)

        return representation
