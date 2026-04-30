from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from app.domain.aggregate.auth import Verification, VerificationType


class VerificationRepository(ABC):

    @abstractmethod
    async def get_by_id(self, verification_id: UUID) -> Optional[Verification]:
        pass

    @abstractmethod
    async def get_by_value_and_type(
        self, value_id: str, verification_type: VerificationType
    ) -> Optional[Verification]:
        pass

    @abstractmethod
    async def create(self, verification: Verification) -> None:
        pass

    @abstractmethod
    async def update(self, verification: Verification) -> None:
        pass

    @abstractmethod
    async def delete(self, verification_id: UUID) -> None:
        pass
