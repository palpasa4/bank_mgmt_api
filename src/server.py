from fastapi import FastAPI
from bank_mgmt_api import admin, users
from database.conn import init_db

app = FastAPI()

init_db()

app.include_router(admin.router)
app.include_router(users.router)
