from app.domain.aggregate.auth import Session, Verification, VerificationType
from app.infrastructure.persistance.mongodb.dao.session_dao import SessionDao
from app.infrastructure.persistance.mongodb.dao.verification_dao import VerificationDao


def from_session_to_dao(session: Session) -> SessionDao:
    return SessionDao(
        id=session.id,
        token=session.token,
        user_id=session.user_id,
        created_at=session.created_at,
        updated_at=session.updated_at,
        expiration_date=session.expiration_date,
        extra_fields=session.extra_fields,
    )


def from_dao_to_session(dao: SessionDao) -> Session:
    return Session(
        id=dao.id,
        token=dao.token,
        user_id=dao.user_id,
        created_at=dao.created_at,
        updated_at=dao.updated_at,
        expiration_date=dao.expiration_date,
        extra_fields=dao.extra_fields,
    )


def from_verification_to_dao(verification: Verification) -> VerificationDao:
    return VerificationDao(
        id=verification.id,
        value_id=verification.value_id,
        type=int(verification.type),
        code=verification.code,
        is_valid=verification.is_valid or False,
        created_at=verification.created_at,
        updated_at=verification.updated_at,
        expiration_date=verification.expiration_date,
    )


def from_dao_to_verification(dao: VerificationDao) -> Verification:
    return Verification(
        id=dao.id,
        value_id=dao.value_id,
        type=VerificationType(dao.type),
        code=dao.code,
        is_valid=dao.is_valid,
        created_at=dao.created_at,
        updated_at=dao.updated_at,
        expiration_date=dao.expiration_date,
    )
