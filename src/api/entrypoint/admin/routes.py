from fastapi import APIRouter, Depends, HTTPException,FastAPI
from fastapi.responses import JSONResponse
from dbschemas.tables import AdminSchema, UserSchema
from api.entrypoint.admin.models import AdminLoginModel, CreateUserModel
from core.auth.auth_handler import sign_jwt
from core.auth.auth_bearer import JWTBearer
from core.logconfig import logger
from src.api.dependencies import db_dependency
from modules.admin.handlers import admin_view_details, admin_view_transactions,create_user, check_valid_admin,check_duplicate_user,check_ifadmin,check_user_details
from starlette.requests import Request
from src.core.handlers.exceptions import *


router = APIRouter()


# admin login
@router.post("/admin/login",tags=["admin_login"],status_code=200)
async def admin_login(model: AdminLoginModel, db: db_dependency):
    admin = check_valid_admin(model, db)
    token = sign_jwt(str(admin.admin_id))
    logger.info(f"Admin login successful for username: {model.username}")
    return token


# admin validation and create user
@router.post("/admin/users", tags=["create_users"],status_code=200)
def create_user_resource(
    model: CreateUserModel, db: db_dependency, id: str = Depends(JWTBearer())
):
    check_ifadmin(id,db)
    check_duplicate_user(model.username,db)
    check_user_details(model)
    create_user(model,db)
    logger.info(f"New user added to table 'user_data' with username: {model.username}")
    logger.info(f"Bank account created successfully to the table 'bank_acc' for '{model.username}'")
    return {"message":f"New user '{model.username}' has been added and Bank account has been created successfully for '{model.username}'"}


#remaining work
# view details
@router.get("/admin/details")
def view_details(db: db_dependency, id: str = Depends(JWTBearer())):
    check_ifadmin(id,db)
    return admin_view_details(db)


# view transactions
@router.get("/admin/transactions")
def view_transactions(db: db_dependency, id: str = Depends(JWTBearer())):
    check_ifadmin(id,db)
    return admin_view_transactions(db)
