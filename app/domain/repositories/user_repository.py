from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.aggregate.user import User, UserRole


class UserRepository(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_group_and_email(self, group: Optional[str], email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_group(self, group: str) -> List[User]:
        pass

    @abstractmethod
    async def get_by_group_and_role(self, group: str, role: UserRole) -> List[User]:
        pass

    @abstractmethod
    async def get_by_role(self, role: UserRole) -> List[User]:
        pass

    @abstractmethod
    async def create(self, user: User) -> None:
        pass

    @abstractmethod
    async def update(self, user: User) -> None:
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> None:
        pass
