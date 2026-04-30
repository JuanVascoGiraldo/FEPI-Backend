from app.domain.aggregate.auth import SessionContainer
from app.domain.services import EncryptionService
from jose import jwt


class EncryptionServiceTestImpl(EncryptionService):

    def __init__(self):
        self.JWT_SECRET = ""
        self.JWT_ALGORITHM = "HS256"

    def hash(self, data):
        return data

    def verify(self, text: str, hashed_text: str):
        return [text == hashed_text, False]

    def get_jwt(self, payload: SessionContainer) -> str:
        data = jwt.encode(payload.model_dump(), self.JWT_SECRET,
                          algorithm=self.JWT_ALGORITHM)
        return data

    def decode_jwt(self, token: str) -> SessionContainer:
        data = jwt.decode(token, self.JWT_SECRET,
                          algorithms=[self.JWT_ALGORITHM])
        return SessionContainer(**data)

