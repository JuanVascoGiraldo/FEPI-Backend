from datetime import datetime, timezone
from fastapi import Depends, Header, HTTPException
from app.domain.aggregate.value_objects.meta import Meta
from app.domain.exceptions import SessionIsnotValidException
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


async def get_session_meta(
    authorization: str | None = Header(default=None, alias="Authorization"),
    timestamp: datetime = Depends(get_utc_timestamp),
) -> Meta:
    from app.application.aggregate.user.commands.validate_session.handler import Handler
    from app.application.aggregate.user.commands.validate_session.request import Request
    if authorization is None:
        raise SessionIsnotValidException("No token provided")
    handler = get_dependency(Handler)
    request = Request(token=authorization)
    return await handler.handle(request, timestamp)
