from typing import List, Optional
from uuid import UUID

from app.config import Config
from app.domain.aggregate.table import Table, TableStatus
from app.domain.repositories.table_repository import TableRepository
from app.domain.services.encryption_service import EncryptionService
from app.infrastructure.persistance.mongodb.clients import MongoClient
from app.infrastructure.persistance.mongodb.dao.table_dao import TableDao
from app.infrastructure.persistance.mongodb.mappers.table import from_dao_to_table, from_table_to_dao


class TableRepositoryImpl(TableRepository):
    COLLECTION = "tables"

    def __init__(
        self,
        mongo_client: MongoClient,
        config: Config,
        encryption_service: EncryptionService,
    ) -> None:
        self.mongo_client = mongo_client
        self.config = config
        self._encrypt = encryption_service.encrypt
        self._decrypt = encryption_service.decrypt

    def _to_doc(self, dao: TableDao) -> dict:
        return dao.to_encrypted_document(self._encrypt)

    def _from_doc(self, document: dict) -> TableDao:
        return TableDao.from_encrypted_document(document, self._decrypt)

    async def get_by_id(self, table_id: UUID) -> Optional[Table]:
        document = await self.mongo_client.find_one(
            self.COLLECTION,
            {"pk": f"{TableDao.PK}{table_id}", "sk": TableDao.SK},
        )
        if document is None:
            return None
        return from_dao_to_table(self._from_doc(document))

    async def get_by_group(self, group: str) -> List[Table]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": TableDao.SK, "group": group},
        )
        return [from_dao_to_table(self._from_doc(d)) for d in documents]

    async def get_ids_by_group(self, group: str) -> List[UUID]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": TableDao.SK, "group": group},
            {"id": 1, "_id": 0},
        )
        return [UUID(str(d["id"])) for d in documents]

    async def get_by_group_and_status(self, group: str, status: TableStatus) -> List[Table]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": TableDao.SK, "group": group, "status": int(status)},
        )
        return [from_dao_to_table(self._from_doc(d)) for d in documents]

    async def create(self, table: Table) -> None:
        dao = from_table_to_dao(table)
        document = self._to_doc(dao)
        document["entity"] = "TABLE"
        await self.mongo_client.insert_one(self.COLLECTION, document)

    async def update(self, table: Table) -> None:
        dao = from_table_to_dao(table)
        document = self._to_doc(dao)
        update_fields = {k: v for k, v in document.items() if k not in ("pk", "sk")}
        await self.mongo_client.update_one(
            self.COLLECTION,
            {"pk": f"{TableDao.PK}{table.id}", "sk": TableDao.SK},
            update_fields,
        )

    async def delete(self, table_id: UUID) -> None:
        await self.mongo_client.delete_one(
            self.COLLECTION,
            {"pk": f"{TableDao.PK}{table_id}", "sk": TableDao.SK},
        )
