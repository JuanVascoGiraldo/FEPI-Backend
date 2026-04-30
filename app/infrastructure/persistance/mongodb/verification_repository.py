from typing import Optional
from uuid import UUID

from app.config import Config
from app.domain.aggregate.auth import Verification, VerificationType
from app.domain.repositories.verification_repository import VerificationRepository
from app.infrastructure.persistance.mongodb.clients import MongoClient
from app.infrastructure.persistance.mongodb.dao.verification_dao import VerificationDao
from app.infrastructure.persistance.mongodb.mappers.auth import (
    from_dao_to_verification,
    from_verification_to_dao,
)


class VerificationRepositoryImpl(VerificationRepository):
    COLLECTION = "verifications"

    def __init__(self, mongo_client: MongoClient, config: Config) -> None:
        self.mongo_client = mongo_client
        self.config = config

    async def get_by_id(self, verification_id: UUID) -> Optional[Verification]:
        document = await self.mongo_client.find_one(
            self.COLLECTION,
            {"pk": f"{VerificationDao.PK}{verification_id}", "sk": VerificationDao.SK},
        )
        if document is None:
            return None
        return from_dao_to_verification(VerificationDao.from_document(document))

    async def get_by_value_and_type(
        self, value_id: str, verification_type: VerificationType
    ) -> Optional[Verification]:
        document = await self.mongo_client.find_one(
            self.COLLECTION,
            {"sk": VerificationDao.SK, "value_id": value_id, "type": int(verification_type)},
        )
        if document is None:
            return None
        return from_dao_to_verification(VerificationDao.from_document(document))

    async def create(self, verification: Verification) -> None:
        dao = from_verification_to_dao(verification)
        document = dao.to_document()
        document["entity"] = "VERIFICATION"
        await self.mongo_client.insert_one(self.COLLECTION, document)

    async def update(self, verification: Verification) -> None:
        dao = from_verification_to_dao(verification)
        update_fields = dao.model_dump(mode="json", exclude={"pk", "sk"})
        await self.mongo_client.update_one(
            self.COLLECTION,
            {"pk": f"{VerificationDao.PK}{verification.id}", "sk": VerificationDao.SK},
            update_fields,
        )

    async def delete(self, verification_id: UUID) -> None:
        await self.mongo_client.delete_one(
            self.COLLECTION,
            {"pk": f"{VerificationDao.PK}{verification_id}", "sk": VerificationDao.SK},
        )
