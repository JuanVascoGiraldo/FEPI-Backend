from app.infrastructure.middlewares import ErrorMiddleWare, ContextMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from app.logger import configure_logging
from app.config import get_settings
from app.application.aggregate import router as aggregate_router
from app.application.commands import router as commands_router
from app.application.public import router as public_router
from app.dependencies import get_dependency
from app.infrastructure.persistance.mongodb.clients import MongoClient
from fastapi import FastAPI, APIRouter


def create_app(on_shutdown=None, on_startup=None):
    configure_logging()
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "https://fepi-frontend.vercel.app",
        "https://fepi-frontend-juan-esteban-vasco-giraldos-projects.vercel.app",
        "https://www.termiapp.email",
    ]
    middlewares = [
        Middleware(CORSMiddleware,
                   allow_origins=allowed_origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   expose_headers=[
                       "Access-Control-Allow-Headers",
                       "X-Process-Time",
                   ]),
        Middleware(ContextMiddleware),
        Middleware(ErrorMiddleWare),
    ]
    async def _ensure_indexes() -> None:
        from logging import getLogger
        logger = getLogger(__name__)
        try:
            await get_dependency(MongoClient).ensure_indexes()
        except Exception as exc:
            logger.error(f"ensure_indexes failed (non-fatal): {exc}")

    if not on_shutdown:
        on_shutdown = []
    if not on_startup:
        on_startup = []
    on_startup.append(_ensure_indexes)
    app = FastAPI(
        title=get_settings().app_name,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        middleware=middlewares,
        openapi_url=get_settings().get_open_api_path(),
    )

    router = APIRouter(prefix="/api")
    router.include_router(commands_router)
    router.include_router(aggregate_router)
    router.include_router(public_router)
    app.include_router(router)
    return app


app = create_app()


if __name__ == "__main__":
    from uvicorn import run
    run("server:app", host=get_settings().host, port=get_settings().port,
        server_header=False, date_header=False,
        reload=get_settings().get_reload(), workers=get_settings().workers)
