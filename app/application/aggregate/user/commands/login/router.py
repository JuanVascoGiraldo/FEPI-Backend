from app.infrastructure.inyections import get_utc_timestamp
from app.dependencies import get_dependency
from fastapi import APIRouter, status, Depends
from .handler import Handler
from .request import Request
from .response import Response

router = APIRouter()


@router.post("/login", response_model=Response, status_code=status.HTTP_200_OK)
async def create(request: Request, timestamp = Depends(get_utc_timestamp)) -> Response:
    handler: Handler = get_dependency(Handler)
    return await handler.handle(request, timestamp)
