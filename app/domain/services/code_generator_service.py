from abc import ABC, abstractmethod


class CodeGeneratorService(ABC):

    @abstractmethod
    def generate_email_code(self) -> str:
        pass

    @abstractmethod
    def generate_session_token(self) -> str:
        pass

    @abstractmethod
    def generate_password_reset_token(self) -> str:
        pass
