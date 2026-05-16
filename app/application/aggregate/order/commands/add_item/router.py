from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.dependencies import get_dependency
from app.infrastructure.inyections import get_session_meta
from app.domain.aggregate.value_objects.meta import Meta

from .handler import Handler
from .request import Request
from .response import Response

router = APIRouter()


@router.post("/{order_id}/items", response_model=Response, status_code=status.HTTP_200_OK)
async def add_item(order_id: UUID, body: Request, session: Meta = Depends(get_session_meta)) -> Response:
    handler: Handler = get_dependency(Handler)
    return await handler.handle(order_id, body, session)
