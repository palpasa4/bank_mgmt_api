from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi.responses import JSONResponse
from src.dbschemas.user import UserSchema
from src.dbschemas.admin import AdminSchema
from src.api.entrypoint.admin.models import AdminLoginModel, CreateUserModel
from src.core.auth.auth_handler import sign_jwt
from src.core.auth.auth_bearer import JWTBearer
from src.core.logconfig import logger
from src.api.dependencies import AnnotatedDatabaseSession, AnnotatedDefaultSettings
from src.api.entrypoint.admin.responses import AdminViewDetails,TokenResponse,UserResponse
from src.modules.admin.handlers import (
    admin_view_details,
    admin_view_transactions,
    admin_view_specific_detail,
    create_user,
    check_valid_admin,
    check_duplicate_user,
    check_ifadmin,
    check_user_details,
)
from starlette.requests import Request
from src.core.handlers.exceptions import *


router = APIRouter(prefix="/admin", tags=["admin"])


# admin login
@router.post("/login/", response_model=TokenResponse, tags=["admin_login"], status_code=200)
async def admin_login(
    model: AdminLoginModel,
    db: AnnotatedDatabaseSession,
    settings: AnnotatedDefaultSettings,
):
    admin = check_valid_admin(model, db)
    token = sign_jwt(str(admin.admin_id), settings)
    logger.info(f"Admin login successful for username: {model.username}")
    return TokenResponse(access_token=token)


# admin validation and create user
@router.post("/users/", response_model=UserResponse, tags=["create_users"], status_code=200)
def create_user_resource(
    model: CreateUserModel, db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())
):
    check_ifadmin(id, db)
    check_duplicate_user(model.username, db)
    check_user_details(model)
    user_info=create_user(model, db)
    logger.info(f"New user added to table 'user_data' with username: {model.username}")
    logger.info(
        f"Bank account created successfully to the table 'bank_acc' for '{model.username}'"
    )
    return UserResponse(message=f"Bank account has been created successfully for new user with username: '{model.username}'",
                        id=user_info[0],
                        password=user_info[1])


# view details
@router.get("/details/")
def view_details(
    request: Request,
    db: AnnotatedDatabaseSession,
    id: str = Depends(JWTBearer()),
):
    check_ifadmin(id, db)
    details = admin_view_details(db)
    logger.info(f"Details viewed by admin with ID: {id}")
    return {"details": details}


# view specific user's details
@router.get("/specific-details/")
def view_specific_detail(
    id: str, db: AnnotatedDatabaseSession, adminid: str = Depends(JWTBearer())
):
    check_ifadmin(adminid, db)
    details = admin_view_specific_detail(id,db)
    logger.info(f"Details of customer with ID: {id} viewed by admin with ID: {adminid}")
    return {"details":details}


# view transactions
@router.get("/transactions/")
def view_transactions(db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())):
    check_ifadmin(id, db)
    transactions = admin_view_transactions(db)
    logger.info(f"Transactions viewed by admin with ID: {id}")
    return {"transactions": transactions}
