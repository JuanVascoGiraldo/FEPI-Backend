import base64

from cryptography.fernet import Fernet
from jose import jwt
from argon2 import PasswordHasher

from app.config import Config
from app.domain.aggregate.auth import SessionContainer
from app.domain.services import EncryptionService

# Stable dev key (all-zero bytes encoded in URL-safe base64).
# Never use this in production — set ENCRYPTION_KEY in the environment.
_DEV_KEY = base64.urlsafe_b64encode(b'\x00' * 32)


class EncryptionServiceImpl(EncryptionService):

    def __init__(self, config: Config) -> None:
        self.hasher = PasswordHasher()
        self.JWT_SECRET = config.JWT_SECRET
        self.JWT_ALGORITHM = config.JWT_ALGORITHM
        raw_key = config.ENCRYPTION_KEY
        key_bytes = raw_key.encode() if raw_key else _DEV_KEY
        self._fernet = Fernet(key_bytes)

    def hash(self, data: str) -> str:
        return self.hasher.hash(data)

    def verify(self, text: str, hashed_text: str):
        try:
            match = self.hasher.verify(hashed_text, text)
        except Exception:
            match = False
        needs_rehash = self.hasher.check_needs_rehash(hashed_text)
        return [match, needs_rehash]

    def get_jwt(self, payload: SessionContainer) -> str:
        data = jwt.encode(payload.model_dump(), self.JWT_SECRET,
                          algorithm=self.JWT_ALGORITHM)
        return data

    def decode_jwt(self, token: str) -> SessionContainer:
        data = jwt.decode(token, self.JWT_SECRET,
                          algorithms=[self.JWT_ALGORITHM])
        return SessionContainer(**data)

    def encrypt(self, text: str) -> str:
        return self._fernet.encrypt(text.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        return self._fernet.decrypt(ciphertext.encode()).decode()
