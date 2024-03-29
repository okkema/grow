from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.contexts.stream import StreamContext
from src.api.contexts.data import DataContext
from src.settings import Settings
from src.api.routes.v1 import sensor


def create_app(settings: Settings):
    app = FastAPI(
        title=settings.OPENAPI_TITLE,
        description=settings.OPENAPI_DESCRIPTION,
        version=settings.OPENAPI_VERSION,
        contact={
            "name": settings.OPENAPI_CONTACT_NAME,
            "url": settings.OPENAPI_CONTACT_URL,
            "email": settings.OPENAPI_CONTACT_EMAIL,
        },
        license_info={
            "name": settings.OPENAPI_LICENSE_NAME,
            "url": settings.OPENAPI_LICENSE_URL,
        },
        docs_url=None,
        redoc_url="/docs",
    )

    # Routes
    app.include_router(sensor.router)

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def on_startup():
        await DataContext.initialize(app, settings)
        await StreamContext.initialize(app, settings)

    @app.on_event("shutdown")
    async def on_shutdown():
        await DataContext.dispose(app)
        await StreamContext.dispose(app)

    return app
