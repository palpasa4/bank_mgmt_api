from fastapi import FastAPI
from database.conn import init_db
from routers import admin_routes, users_routes, info_routes

app = FastAPI()

init_db()

app.include_router(admin_routes.router)
app.include_router(users_routes.router)
app.include_router(info_routes.router)
