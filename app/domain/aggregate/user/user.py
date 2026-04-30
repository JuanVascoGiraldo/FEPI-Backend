from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

from .user_role import UserRole
from .email import Email


class User(BaseModel):
    id: UUID
    group: str
    first_name: str
    last_name: str
    email: Email
    password_hash: str
    role: UserRole
    is_active: bool = True
    phone: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def is_superadmin(self) -> bool:
        return self.role == UserRole.SUPERADMIN

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def is_waiter(self) -> bool:
        return self.role == UserRole.WAITER

    def belongs_to_group(self, group: str) -> bool:
        return self.group == group

    def can_manage_group(self, group: str) -> bool:
        """SUPERADMIN manages any group; ADMIN manages only their own."""
        if self.is_superadmin():
            return True
        return self.belongs_to_group(group) and self.is_admin()
