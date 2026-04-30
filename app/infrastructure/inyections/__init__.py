from datetime import datetime, timezone
from urllib import request
from fastapi import Header, HTTPException
from app.domain.aggregate.value_objects.meta import Meta
from app.domain.exceptions import SessionIsnotValidException
from app.application.aggregate.user.commands.validate_session.handler import Handler
from app.application.aggregate.user.commands.validate_session.request import Request
from app.dependencies import get_dependency


def get_utc_timestamp(timestamp: str | None = Header(default=None, alias="TIMESTAMP")) -> datetime:
    if not timestamp:
        return datetime.now(timezone.utc)

    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid TIMESTAMP header format") from exc

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed.astimezone(timezone.utc)


async def get_session_meta() -> Meta:
    token = Header(default=None, alias="Authorization")
    if token is None:
        raise SessionIsnotValidException("No token provided")
    handler = get_dependency(Handler)
    request = Request(token=token)
    response = await handler.handle(request, get_utc_timestamp())
    return response
