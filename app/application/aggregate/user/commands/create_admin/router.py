from fastapi import APIRouter, status, Depends

from app.dependencies import get_dependency
from app.infrastructure.inyections import get_session_meta
from app.domain.aggregate.value_objects.meta import Meta

from .handler import Handler
from .request import Request
from .response import Response

router = APIRouter()


@router.post("/admin", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create_admin(request: Request, session: Meta = Depends(get_session_meta)) -> Response:
    handler: Handler = get_dependency(Handler)
    return await handler.handle(request, session)
