from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class Response(BaseModel):
    id: UUID
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
