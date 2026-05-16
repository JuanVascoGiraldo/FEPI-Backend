import asyncio
from datetime import datetime, timezone
from typing import AsyncGenerator

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse, Response

from app.dependencies import get_dependency
from app.infrastructure.events.event_bus import EventBus

router = APIRouter(prefix="/events")


async def _validate_token(token: str):
    from app.application.aggregate.user.commands.validate_session.handler import Handler
    from app.application.aggregate.user.commands.validate_session.request import Request
    try:
        handler = get_dependency(Handler)
        return await handler.handle(Request(token=token), datetime.now(timezone.utc))
    except Exception:
        return None


@router.get("/stream")
async def stream_events(token: str = Query(...)):
    session = await _validate_token(token)
    if not session or not session.group:
        return Response(content="Unauthorized", status_code=401)

    event_bus = get_dependency(EventBus)
    group = session.group
    queue = event_bus.subscribe(group)

    async def generate() -> AsyncGenerator[str, None]:
        try:
            yield ": connected\n\n"
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=25)
                    yield event.to_sse()
                except asyncio.TimeoutError:
                    yield ": heartbeat\n\n"
        finally:
            event_bus.unsubscribe(group, queue)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
