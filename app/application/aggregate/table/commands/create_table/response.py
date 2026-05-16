from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Response(BaseModel):
    id: UUID
    group: str
    number: str
    description: Optional[str] = None
    status: int
    created_at: datetime
    updated_at: datetime
