from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.aggregate.auth import Session


class SessionRepository(ABC):

    @abstractmethod
    async def get_by_id(self, session_id: UUID) -> Optional[Session]:
        pass

    @abstractmethod
    async def get_by_token(self, token: str) -> Optional[Session]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Session]:
        pass

    @abstractmethod
    async def create(self, session: Session) -> None:
        pass

    @abstractmethod
    async def update(self, session: Session) -> None:
        pass

    @abstractmethod
    async def delete(self, session_id: UUID) -> None:
        pass

    @abstractmethod
    async def delete_by_user_id(self, user_id: UUID) -> None:
        pass
