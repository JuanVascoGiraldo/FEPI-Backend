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

