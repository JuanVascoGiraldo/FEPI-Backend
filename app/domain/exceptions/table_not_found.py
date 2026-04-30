from .base_domain_exception import BaseDomainException


class TableNotFoundException(BaseDomainException):
    def __init__(self, table_id: str) -> None:
        super().__init__(
            message=f"Table with id '{table_id}' was not found.",
            response_code=404,
            name="table_not_found",
        )
