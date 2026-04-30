from .base_domain_exception import BaseDomainException


class IsNotAuthorizedException(BaseDomainException):
    def __init__(self):
        super().__init__(
            message="User is not authorized to perform this action",
            response_code=401
        )
        