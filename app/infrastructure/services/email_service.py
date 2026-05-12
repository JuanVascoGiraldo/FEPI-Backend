import resend
from datetime import datetime, timezone
from logging import Logger

from app.config import Config
from app.domain.aggregate.user import Email
from app.domain.services import EmailService, RenderService


class EmailServiceImpl(EmailService):

    def __init__(self, config: Config, logger: Logger, render_service: RenderService) -> None:
        self._logger = logger
        self._from = config.EMAIL_FROM
        self._app_url = config.APP_URL
        self._render_service = render_service
        resend.api_key = config.RESEND_API_KEY

    async def send_welcome(
        self,
        to: Email,
        name: str,
        role: str,
        group: str | None = None,
        password: str | None = None,
    ) -> None:
        html = self._render_service.render(
            "welcome.html",
            {
                "name": name,
                "role": role,
                "group": group or "",
                "password": password or "",
                "app_url": self._app_url,
                "year": datetime.now(timezone.utc).year,
            },
        )
        params: resend.Emails.SendParams = {
            "from": self._from,
            "to": [str(to)],
            "subject": f"Welcome to TERMI, {name}!",
            "html": html,
        }
        try:
            resend.Emails.send(params)
        except Exception as exc:
            self._logger.error("Failed to send welcome email to %s: %s", to, exc)
            raise
