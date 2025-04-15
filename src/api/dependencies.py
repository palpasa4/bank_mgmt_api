from h11 import Request
from src.config.database import get_db_session
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.settings import DefaultSettings

def get_default_settings(request: Request)->DefaultSettings:
    return request.app.state.settings.default

AnnotatedDatabaseSession = Annotated[Session, Depends(get_db_session)]
AnotatedDefaultSettings = Annotated[DefaultSettings, Depends(get_default_settings)]