from app.domain.aggregate.user import Email
from app.domain.services import EmailService
from app.config import Config
from logging import Logger


class EmailServiceImpl(EmailService):

    def __init__(
        self,
        config: Config,
        logger: Logger,
    ):
        self.logger = logger
        self.email_from = "fepi"
        self.config = config

    async def send_start_email(self, email: Email) -> None:
        pass
