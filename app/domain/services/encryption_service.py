from app.domain.aggregate.auth import SessionContainer
from abc import ABC, abstractmethod
from typing import Tuple


class EncryptionService(ABC):

    @abstractmethod
    def hash(self, text: str) -> str:
        pass

    @abstractmethod
    def verify(self, text: str, hashed_text: str) -> Tuple[bool, bool]:
        pass

    @abstractmethod
    def get_jwt(self, payload: SessionContainer) -> str:
        pass

    @abstractmethod
    def decode_jwt(self, token: str) -> SessionContainer:
        pass

    @abstractmethod
    def encrypt(self, text: str) -> str:
        """Symmetrically encrypt a plaintext string. Returns a URL-safe base64 ciphertext."""
        pass

    @abstractmethod
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt a ciphertext produced by encrypt(). Returns the original plaintext."""
        pass
