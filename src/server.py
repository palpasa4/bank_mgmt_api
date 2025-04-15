from contextlib import asynccontextmanager
from src.config.database import init_db
from fastapi import FastAPI
from src.api.entrypoint.admin import routes as admin_routes
from src.api.entrypoint.user import routes as user_routes
from src.core.middleware import CustomExceptionMiddleware
from src.config.settings import AppSettings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = AppSettings() 
    print(app.state.settings)
    print("Starting Server")
    init_db(app.state.settings.database)
    yield
    print("Stopping Server")


def init_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    # include routers
    app.include_router(admin_routes.router)
    # app.include_router(user_routes.router)

    # user middlewares
    app.add_middleware(CustomExceptionMiddleware)

    return app


app = init_app()
