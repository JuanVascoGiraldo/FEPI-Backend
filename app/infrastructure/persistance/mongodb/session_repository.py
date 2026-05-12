from typing import List, Optional
from uuid import UUID

from app.config import Config
from app.domain.aggregate.auth import Session
from app.domain.repositories.session_repository import SessionRepository
from app.domain.services.encryption_service import EncryptionService
from app.infrastructure.persistance.mongodb.clients import MongoClient
from app.infrastructure.persistance.mongodb.dao.session_dao import SessionDao
from app.infrastructure.persistance.mongodb.dao.index_dao import IndexDao
from app.infrastructure.persistance.mongodb.mappers.auth import from_dao_to_session, from_session_to_dao

TOKEN_PK_PREFIX = "TOKEN#"
SESSION_SK_PREFIX = "SESSION#"


class SessionRepositoryImpl(SessionRepository):
    COLLECTION = "sessions"
    INDEX_COLLECTION = "indexes"

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

    def _to_doc(self, dao: SessionDao) -> dict:
        return dao.to_encrypted_document(self._encrypt)

    def _from_doc(self, document: dict) -> SessionDao:
        return SessionDao.from_encrypted_document(document, self._decrypt)

    async def get_by_id(self, session_id: UUID) -> Optional[Session]:
        document = await self.mongo_client.find_one(
            self.COLLECTION,
            {"pk": f"{SessionDao.PK}{session_id}", "sk": SessionDao.SK},
        )
        if document is None:
            return None
        return from_dao_to_session(self._from_doc(document))

    async def get_by_token(self, token: str) -> Optional[Session]:
        # The index pk always stores the plaintext token — no encryption needed here.
        index = await self.mongo_client.find_one(
            self.INDEX_COLLECTION,
            {"pk": f"{TOKEN_PK_PREFIX}{token}"},
        )
        if index is None:
            return None
        session_id = UUID(index["sk"].replace(SESSION_SK_PREFIX, "", 1))
        return await self.get_by_id(session_id)

    async def get_by_user_id(self, user_id: UUID) -> List[Session]:
        documents = await self.mongo_client.find_many(
            self.COLLECTION,
            {"sk": SessionDao.SK, "user_id": str(user_id)},
        )
        return [from_dao_to_session(self._from_doc(d)) for d in documents]

    async def create(self, session: Session) -> None:
        dao = from_session_to_dao(session)
        document = self._to_doc(dao)
        document["entity"] = "SESSION"
        await self.mongo_client.insert_one(self.COLLECTION, document)

        # Index stores the plaintext token so it can be looked up without decryption.
        token_index = IndexDao(
            pk=f"{TOKEN_PK_PREFIX}{session.token}",
            sk=f"{SESSION_SK_PREFIX}{session.id}",
        )
        index_doc = token_index.to_document()
        index_doc["entity"] = "SESSION_TOKEN_INDEX"
        await self.mongo_client.insert_one(self.INDEX_COLLECTION, index_doc)

    async def update(self, session: Session) -> None:
        dao = from_session_to_dao(session)
        document = self._to_doc(dao)
        update_fields = {k: v for k, v in document.items() if k not in ("pk", "sk")}
        await self.mongo_client.update_one(
            self.COLLECTION,
            {"pk": f"{SessionDao.PK}{session.id}", "sk": SessionDao.SK},
            update_fields,
        )

    async def delete(self, session_id: UUID) -> None:
        session = await self.get_by_id(session_id)
        await self.mongo_client.delete_one(
            self.COLLECTION,
            {"pk": f"{SessionDao.PK}{session_id}", "sk": SessionDao.SK},
        )
        if session:
            # Use plaintext token to delete the index entry.
            await self.mongo_client.delete_one(
                self.INDEX_COLLECTION,
                {"pk": f"{TOKEN_PK_PREFIX}{session.token}"},
            )

    async def delete_by_user_id(self, user_id: UUID) -> None:
        sessions = await self.get_by_user_id(user_id)
        for session in sessions:
            await self.delete(session.id)
