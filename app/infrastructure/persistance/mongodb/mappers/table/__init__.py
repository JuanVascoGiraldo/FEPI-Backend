from app.domain.aggregate.table import Table, TableStatus
from app.infrastructure.persistance.mongodb.dao.table_dao import TableDao


def from_table_to_dao(table: Table) -> TableDao:
    return TableDao(
        id=table.id,
        group=table.group,
        number=table.number,
        description=table.description,
        status=int(table.status),
        created_at=table.created_at,
        updated_at=table.updated_at,
    )


def from_dao_to_table(dao: TableDao) -> Table:
    return Table(
        id=dao.id,
        group=dao.group,
        number=dao.number,
        description=dao.description,
        status=TableStatus(dao.status),
        created_at=dao.created_at,
        updated_at=dao.updated_at,
    )
