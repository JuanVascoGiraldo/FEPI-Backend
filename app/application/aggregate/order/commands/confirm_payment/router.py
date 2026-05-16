from uuid import UUID

from fastapi import APIRouter, status, Depends

from app.dependencies import get_dependency
from app.infrastructure.inyections import get_session_meta
from app.domain.aggregate.value_objects.meta import Meta

from .handler import Handler
from .response import Response

router = APIRouter()


@router.post("/{order_id}/payments/{payment_id}/confirm", response_model=Response, status_code=status.HTTP_200_OK)
async def confirm_payment(
    order_id: UUID,
    payment_id: UUID,
    session: Meta = Depends(get_session_meta),
) -> Response:
    handler: Handler = get_dependency(Handler)
    return await handler.handle(order_id, payment_id, session)
