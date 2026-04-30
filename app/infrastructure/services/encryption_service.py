from app.domain.aggregate.auth import SessionContainer
from app.domain.services import EncryptionService
from app.config import Config
from jose import jwt
from argon2 import PasswordHasher
from hashlib import sha256


class EncryptionServiceImpl(EncryptionService):

    def __init__(self, config: Config) -> None:
        self.hasher = PasswordHasher()
        self.JWT_SECRET = config.JWT_SECRET
        self.JWT_ALGORITHM = config.JWT_ALGORITHM

    def hash(self, data):
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
