from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.domain.aggregate.user import UserRole


class Meta(BaseModel):
    user_id: UUID
    session_id: UUID
    role: UserRole
    group: str | None = None
    timestamp: datetime
    jwt: str
