from pydantic import BaseModel
from typing import Optional
import hashlib


class SessionContainer(BaseModel):
    id: str
    token: str
    user_id: str
    session_id: str
    role: int
    expire_at: str
    created_at: str
    updated_at: str
    signature: Optional[str] = None

    def get_signature(self) -> str:
        if self.signature is None:
            self.signature = hashlib.sha256(str(self.id).encode()).hexdigest()
        return self.signature

    @classmethod
    def from_session_model(cls, session, user) -> 'SessionContainer':
        return cls(
            id=str(session.id),
            user_id=str(user.id),
            expire_at=session.expiration_date.isoformat(),
            created_at=session.created_at.isoformat(),
            updated_at=session.updated_at.isoformat(),
            token=session.token,
            role=int(user.role),
            session_id=str(session.id),
        )

    def payload(self, include_signature: bool = True) -> dict:
        payload = {
            'id': str(self.id),
            'user_id': str(self.user_id),
            'role': self.role,
            'expire_at': self.expire_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'session_id': self.session_id,
        }
        if include_signature:
            payload['signature'] = self.get_signature()
        return payload

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, SessionContainer):
            return self.get_signature() == __value.get_signature()
        return super().__eq__(__value)
