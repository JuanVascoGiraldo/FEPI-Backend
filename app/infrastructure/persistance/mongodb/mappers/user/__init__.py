from app.domain.aggregate.user import User, UserRole, Email
from app.infrastructure.persistance.mongodb.dao.user_dao import UserDao


def from_user_to_dao(user: User) -> UserDao:
    return UserDao(
        id=user.id,
        group=user.group,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email.value,
        password_hash=user.password_hash,
        role=int(user.role),
        is_active=user.is_active,
        phone=user.phone,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def from_dao_to_user(dao: UserDao) -> User:
    return User(
        id=dao.id,
        group=dao.group,
        first_name=dao.first_name,
        last_name=dao.last_name,
        email=Email(value=dao.email),
        password_hash=dao.password_hash,
        role=UserRole(dao.role),
        is_active=dao.is_active,
        phone=dao.phone,
        created_at=dao.created_at,
        updated_at=dao.updated_at,
    )
