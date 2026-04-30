from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class Group(BaseModel):
    id: UUID
    name: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
