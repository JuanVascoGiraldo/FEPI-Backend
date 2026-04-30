from bson import timestamp
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime, timezone

from .verification_type import VerificationType


class Verification(BaseModel):
    id: UUID
    value_id: str  # email, phone number or entity ID being verified
    type: VerificationType
    code: str
    is_valid: Optional[bool] = False
    created_at: datetime
    updated_at: datetime
    expiration_date: datetime

    def is_expired(self, timestamp: datetime) -> bool:
        return timestamp > self.expiration_date

    def validate_code(self, code: str, timestamp: datetime) -> bool:
        """Returns True and marks as used when the code matches and is not expired."""
        if self.is_expired(timestamp) or self.is_valid:
            return False
        if self.code != code:
            return False
        self.is_valid = True
        self.updated_at = timestamp
        return True

    def invalidate(self, timestamp: datetime) -> None:
        """Force-invalidates this verification (e.g. when a new code is issued)."""
        self.is_valid = False
        self.updated_at = timestamp
