from datetime import datetime
from pydantic import BaseModel
from typing import List
from uuid import UUID


class GroupItem(BaseModel):
    id: UUID
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class Response(BaseModel):
    groups: List[GroupItem]
