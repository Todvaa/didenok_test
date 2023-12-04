import base64
import hashlib
import os
from typing import Union

from cryptography.fernet import Fernet, InvalidToken
from dotenv import load_dotenv

load_dotenv()


class PasswordEncryptor:
    KEY = base64.urlsafe_b64encode(
        hashlib.sha256(os.getenv('PASSWORD_SECRET_KEY').encode()).digest()
    )
    CIPHER_SUITE = Fernet(KEY)

    def encrypt_password(self, password: str) -> bytes:
        """Encrypt the provided password using
         the Fernet encryption algorithm."""

        return self.CIPHER_SUITE.encrypt(password.encode())

    def decrypt_password(
            self, encoded_password: Union[memoryview, bytes]
    ) -> str:
        """Decrypts the provided encoded password using
         the Fernet encryption algorithm."""

        try:
            if isinstance(encoded_password, memoryview):
                encoded_password = encoded_password.tobytes()

            return self.CIPHER_SUITE.decrypt(encoded_password).decode('utf-8')
        except InvalidToken:
            # todo: add logging in the future
            raise ValueError('Cannot decrypt string')


password_encryptor = PasswordEncryptor()
