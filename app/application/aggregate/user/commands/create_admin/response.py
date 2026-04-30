from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Response(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    role: int
    group: Optional[str]
    is_active: bool
    phone: Optional[str]
    created_at: datetime
