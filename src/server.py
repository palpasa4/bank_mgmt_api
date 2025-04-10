from fastapi import FastAPI
from api.entrypoint.admin import routes as admin_routes
from api.entrypoint.user import routes as user_routes
from src.api.dependencies import init_db
from src.core.handlers.middleware import CustomExceptionMiddleware


app = FastAPI()

init_db()

app.include_router(admin_routes.router)
app.include_router(user_routes.router)

app.add_middleware(CustomExceptionMiddleware)