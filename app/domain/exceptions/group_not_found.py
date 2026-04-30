from .base_domain_exception import BaseDomainException


class GroupNotFoundException(BaseDomainException):
    def __init__(self, name: str) -> None:
        super().__init__(
            message=f"Group '{name}' not found.",
            response_code=404,
            name="group_not_found",
        )
