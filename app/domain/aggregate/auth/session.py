from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime, timezone


class Session(BaseModel):
    id: UUID
    token: str
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    expiration_date: datetime
    extra_fields: dict = Field(default_factory=dict)

    def is_expired(self, timestamp: datetime) -> bool:
        return timestamp > self.expiration_date

    def is_active(self, timestamp: datetime) -> bool:
        return not self.is_expired(timestamp)

    def refresh(self, new_expiration: datetime, timestamp: datetime) -> None:
        self.expiration_date = new_expiration
        self.updated_at = timestamp
