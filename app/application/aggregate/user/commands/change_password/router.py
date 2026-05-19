from fastapi import APIRouter, Depends, status

from app.dependencies import get_dependency
from app.infrastructure.inyections import get_session_meta
from app.domain.aggregate.value_objects.meta import Meta

from .handler import Handler
from .request import Request
from .response import Response

router = APIRouter()


@router.patch("/me/password", response_model=Response, status_code=status.HTTP_200_OK)
async def change_password(
    request: Request, session: Meta = Depends(get_session_meta)
) -> Response:
    handler: Handler = get_dependency(Handler)
    return await handler.handle(request, session)
