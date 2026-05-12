from abc import ABC, abstractmethod

from app.domain.aggregate.user import Email


class EmailService(ABC):

    @abstractmethod
    async def send_welcome(
        self,
        to: Email,
        name: str,
        role: str,
        group: str | None = None,
        password: str | None = None,
    ) -> None:
        """Send a welcome email when a new user account is created."""
        pass
