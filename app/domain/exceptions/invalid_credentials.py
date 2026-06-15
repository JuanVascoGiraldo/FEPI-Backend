from .base_domain_exception import BaseDomainException


class InvalidCredentialsException(BaseDomainException):
    def __init__(self) -> None:
        super().__init__(
            message="Correo electrónico o contraseña incorrectos.",
            response_code=401,
            name="invalid_credentials",
        )
