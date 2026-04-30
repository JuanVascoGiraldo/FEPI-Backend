from app.domain.services import CodeGeneratorService
import secrets
import string


class CodeGeneratorServiceImpl(CodeGeneratorService):
    def __init__(self) -> None:
        self.alphabet = string.ascii_letters + string.digits

    def generate_email_code(self) -> str:
        return ''.join(secrets.choice(string.digits) for _ in range(6))

    def generate_phone_code(self) -> str:
        return ''.join(secrets.choice(string.digits) for _ in range(6))

    def generate_session_token(self) -> str:
        return ''.join(secrets.choice(self.alphabet) for _ in range(32))

    def generate_password_reset_token(self) -> str:
        return ''.join(secrets.choice(self.alphabet) for _ in range(32))

