from fastapi import APIRouter, Depends
from core.handlers.response_handler import json_response
from core.auth.helpers import check_role
from core.auth.auth_bearer import JWTBearer
from core.handlers.logger_config import logger
from database.conn import db_dependency
from database.users_db import (
    admin_view_details,
    user_view_details,
    admin_view_transactions,
    user_view_transactions,
)

router = APIRouter()


# view details
@router.get("/details")
def view_details(db: db_dependency, user_id: str = Depends(JWTBearer())):
    if check_role(user_id, db) == "admin":
        return admin_view_details(db)
    return user_view_details(user_id, db)


# view transactions
@router.get("/transactions")
def view_transactions(db: db_dependency, user_id: str = Depends(JWTBearer())):
    if check_role(user_id, db) == "admin":
        return admin_view_transactions(db)
    return user_view_transactions(user_id, db)
