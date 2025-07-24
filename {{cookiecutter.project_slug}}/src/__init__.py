from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from tortoise import Tortoise

from core.dependency import get_current_username
from core.exceptions import SettingNotFound
from core.init_app import (
    init_data,
    make_middlewares,
    register_exceptions,
    register_routers,
)

try:
    from settings.config import settings
except ImportError as e:
    raise SettingNotFound("Can not import settings") from e


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_data()
    yield
    await Tortoise.close_connections()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.VERSION,
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
        middleware=make_middlewares(),
        lifespan=lifespan,
    )

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html(
        username: str = Depends(get_current_username),
    ):
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=app.title + " - Swagger UI",
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        )

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html(username: str = Depends(get_current_username)):
        return get_redoc_html(
            openapi_url="/openapi.json",
            title=app.title + " - ReDoc",
        )

    @app.get("/openapi.json", include_in_schema=False)
    async def get_open_api_endpoint(
        username: str = Depends(get_current_username),
    ):
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        return openapi_schema

    register_exceptions(app)
    register_routers(app, prefix="/api")
    return app


app = create_app()
