from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi.responses import JSONResponse
from src.dbschemas.tables import AdminSchema, UserSchema
from src.api.entrypoint.admin.models import AdminLoginModel, CreateUserModel
from src.core.auth.auth_handler import sign_jwt
from src.core.auth.auth_bearer import JWTBearer
from src.core.logconfig import logger
from src.api.dependencies import AnnotatedDatabaseSession, AnotatedDefaultSettings
from src.api.entrypoint.admin.responses import AdminViewDetails
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
from src.core.exceptions import *


router = APIRouter(prefix="/admin", tags=["admin"])


# admin login
@router.post("/login/", tags=["admin_login"], status_code=200)
async def admin_login(request: Request, model: AdminLoginModel, db: AnnotatedDatabaseSession):
    admin = check_valid_admin(model, db)
    token = sign_jwt(str(admin.admin_id), request.app.state.settings.default)
    logger.info(f"Admin login successful for username: {model.username}")
    return token


# admin validation and create user
@router.post("/users/", tags=["create_users"], status_code=200)
def create_user_resource(
    model: CreateUserModel, db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())
):
    check_ifadmin(id, db)
    check_duplicate_user(model.username, db)
    check_user_details(model)
    create_user(model, db)
    logger.info(f"New user added to table 'user_data' with username: {model.username}")
    logger.info(
        f"Bank account created successfully to the table 'bank_acc' for '{model.username}'"
    )
    return {
        "message": f"New user '{model.username}' has been added and Bank account has been created successfully for '{model.username}'"
    }


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
@router.get("/details/")
def view_specific_detail(id:str,db: AnnotatedDatabaseSession, adminid:str=Depends(JWTBearer())):
    check_ifadmin(adminid, db)
    details=admin_view_specific_detail(db)
    logger.info(f"Details of customer with ID: {id} viewed by admin with ID: {adminid}")


# view transactions
@router.get("/transactions/")
def view_transactions(db: AnnotatedDatabaseSession, id: str = Depends(JWTBearer())):
    check_ifadmin(id, db)
    transactions = admin_view_transactions(db)
    logger.info(f"Transactions viewed by admin with ID: {id}")
    return {"transactions": transactions}
