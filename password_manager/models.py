from django.contrib.auth import get_user_model
from django.db import models

from password_manager.utils import password_encryptor

User = get_user_model()


class PasswordManager(models.Model):
    password = models.BinaryField()
    service_name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_manager'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['service_name', 'user'],
                name='unique service name'
            )
        ]
        ordering = ['id']

    def __str__(self):
        return f'{self.user.id}/{self.service_name}'

    def save(self, *args, **kwargs):
        self.password = password_encryptor.encrypt_password(self.password)
        super().save(*args, **kwargs)

    @property
    def decrypted_password(self):
        return password_encryptor.decrypt_password(self.password)
