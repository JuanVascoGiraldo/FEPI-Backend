import resend
from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional
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
            "subject": f"Bienvenido a TERMI, {name}!",
            "html": html,
        }
        try:
            resend.Emails.send(params)
        except Exception as exc:
            self._logger.error("Failed to send welcome email to %s: %s", to, exc)
            raise

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
        total = amount + tip
        method_label = "Efectivo" if payment_method == "cash" else "Tarjeta"

        items_rows = ""
        for item in items:
            subtotal = item.unit_price * item.quantity
            items_rows += (
                f'<tr>'
                f'<td style="padding:10px 16px;border-bottom:1px solid #e2e8f0;font-size:14px;color:#0f172a;">{item.name}</td>'
                f'<td style="padding:10px 16px;border-bottom:1px solid #e2e8f0;font-size:14px;color:#64748b;text-align:center;">{item.quantity}</td>'
                f'<td style="padding:10px 16px;border-bottom:1px solid #e2e8f0;font-size:14px;color:#64748b;text-align:right;">${item.unit_price:.2f}</td>'
                f'<td style="padding:10px 16px;border-bottom:1px solid #e2e8f0;font-size:14px;font-weight:600;color:#0f172a;text-align:right;">${subtotal:.2f}</td>'
                f'</tr>'
            )

        fiscal_row = ""
        if fiscal_info:
            fiscal_row = (
                f'<tr>'
                f'<td style="padding:8px 0;font-size:13px;color:#64748b;">RFC / Datos fiscales</td>'
                f'<td style="padding:8px 0;font-size:13px;color:#0f172a;font-weight:600;">{fiscal_info}</td>'
                f'</tr>'
            )

        html = self._render_service.render(
            "receipt.html",
            {
                "name": name,
                "table_number": table_number,
                "amount": f"{amount:.2f}",
                "tip": f"{tip:.2f}",
                "total": f"{total:.2f}",
                "payment_method": method_label,
                "fiscal_row": fiscal_row,
                "items_rows": items_rows,
                "year": datetime.now(timezone.utc).year,
            },
        )
        params: resend.Emails.SendParams = {
            "from": self._from,
            "to": [to],
            "subject": "Tu comprobante de pago — TERMI",
            "html": html,
        }
        try:
            resend.Emails.send(params)
            self._logger.info("Receipt sent to %s", to)
        except Exception as exc:
            self._logger.error("Failed to send receipt to %s: %s", to, exc)
            raise
