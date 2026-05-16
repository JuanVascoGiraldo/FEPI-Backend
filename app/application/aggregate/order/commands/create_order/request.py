from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class Request(BaseModel):
    table_id: UUID
    notes: Optional[str] = None
