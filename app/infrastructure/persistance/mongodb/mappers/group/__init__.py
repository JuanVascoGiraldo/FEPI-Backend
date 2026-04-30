from app.domain.aggregate.group import Group
from app.infrastructure.persistance.mongodb.dao.group_dao import GroupDao


def from_group_to_dao(group: Group) -> GroupDao:
    return GroupDao(
        id=group.id,
        name=group.name,
        is_active=group.is_active,
        created_at=group.created_at,
        updated_at=group.updated_at,
    )


def from_dao_to_group(dao: GroupDao) -> Group:
    return Group(
        id=dao.id,
        name=dao.name,
        is_active=dao.is_active,
        created_at=dao.created_at,
        updated_at=dao.updated_at,
    )
