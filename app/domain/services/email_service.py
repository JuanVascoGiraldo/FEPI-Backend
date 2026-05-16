from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional

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

    @abstractmethod
    async def send_receipt(
        self,
        to: str,
        name: str,
        table_number: str,
        amount: Decimal,
        tip: Decimal,
        items: List,
        fiscal_info: Optional[str],
        payment_method: str,
    ) -> None:
        """Send a payment receipt to the customer."""
        pass
