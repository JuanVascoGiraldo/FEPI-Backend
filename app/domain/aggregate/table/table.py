from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime, timezone

from .table_status import TableStatus


class Table(BaseModel):
    id: UUID
    group: str  # restaurant identifier this table belongs to
    number: str  # human-readable identifier (e.g. "5", "VIP-1")
    capacity: int  # max diners; used for seating management
    description: Optional[str] = None  # e.g. "Terrace", "VIP Room"
    status: TableStatus = TableStatus.ACTIVE
    created_at: datetime
    updated_at: datetime

    def activate(self, timestamp: datetime) -> None:
        self.status = TableStatus.ACTIVE
        self.updated_at = timestamp

    def deactivate(self, timestamp: datetime) -> None:
        self.status = TableStatus.INACTIVE
        self.updated_at = timestamp

    def is_active(self) -> bool:
        return self.status == TableStatus.ACTIVE
