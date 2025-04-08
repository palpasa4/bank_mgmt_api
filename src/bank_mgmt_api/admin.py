from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from database.tables import AdminSchema, UserSchema
from models.request_models import Login, User
from core.handlers.response_handler import json_response
from core.auth.auth_handler import sign_jwt
from core.auth.helpers import check_password, check_role
from core.auth.auth_bearer import JWTBearer
from core.handlers.logger_config import logger
from database.conn import db_dependency
from core.handlers.users_db import add_newuser,admin_view_details,admin_view_transactions
from starlette.requests import Request


router = APIRouter()


# admin login
@router.post("/admin/login")
async def admin_login(model: Login, db: db_dependency):
    logger.info(f"Admin login request received for username: {model.username}")
    db_admin = db.query(AdminSchema).filter_by(username=model.username).first()
    if db_admin is None or not check_password(model.password, str(db_admin.password)):
        logger.warning(f"Login failed for username: {model.username} - Invalid username or password.")
        raise HTTPException(status_code=401, detail="Invalid username or password")
    logger.info(f"Admin login successful for username: {model.username}")
    token= sign_jwt(str(db_admin.admin_id))
    logger.info(f"JWT token generated successfully for admin ID: {db_admin.admin_id}")
    return token


# admin validation and create user
@router.post("/admin/users", tags=["create_users"])
def create_user_resource(
    model: User, db: db_dependency, user_id: str = Depends(JWTBearer())
):
    if check_role(user_id, db) != "admin":
        raise HTTPException(status_code=403, detail="User not allowed!")
    existing_user = db.query(UserSchema).filter(UserSchema.username == model.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists!")
    if len(model.username) < 7:
        raise HTTPException(status_code=400, detail="Username must be at least 7 characters long!")
    if model.opening_balance < 500:
        raise HTTPException(status_code=400, detail="Minimum opening balance is 500!")
    return add_newuser(model,db)


# view details
@router.get("/admin/details")
def view_details(db: db_dependency, user_id: str = Depends(JWTBearer())):
    if check_role(user_id, db) != "admin":
        raise HTTPException(status_code=403, detail="User not allowed!")
    return admin_view_details(db)


# view transactions
@router.get("/admin/transactions")
def view_transactions(db: db_dependency, user_id: str = Depends(JWTBearer())):
    if check_role(user_id, db) != "admin":
        raise HTTPException(status_code=403, detail="User not allowed!")
    return admin_view_transactions(db)