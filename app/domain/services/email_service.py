from app.domain.aggregate.user import Email
from abc import ABC, abstractmethod


class EmailService(ABC):

    @abstractmethod
    async def send_start_email(self, email: Email) -> None:
        pass
