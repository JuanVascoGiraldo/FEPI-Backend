from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.dependencies import get_dependency
from app.infrastructure.inyections import get_session_meta
from app.domain.aggregate.value_objects.meta import Meta

from .handler import Handler
from .response import Response

router = APIRouter()


@router.post("/{order_id}/items/{item_id}/deliver", response_model=Response, status_code=status.HTTP_200_OK)
async def mark_item_delivered(
    order_id: UUID,
    item_id: UUID,
    session: Meta = Depends(get_session_meta),
) -> Response:
    handler: Handler = get_dependency(Handler)
    return await handler.handle(order_id, item_id, session)
