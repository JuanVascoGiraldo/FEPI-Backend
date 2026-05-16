from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class WaiterItem(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    group: Optional[str]
    is_active: bool
    phone: Optional[str]
    created_at: datetime
    updated_at: datetime


class Response(BaseModel):
    waiters: List[WaiterItem]
