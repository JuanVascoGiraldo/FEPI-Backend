from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


class Response(BaseModel):
    user_id: UUID
    session_id: UUID
    group: Optional[str]
    role: int
    jwt: str
    expiration_date: datetime
