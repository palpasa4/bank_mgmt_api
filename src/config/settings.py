# from config.database import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
# from dotenv import load_dotenv
# import os
from ast import main
from pydantic import BaseModel,  SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str 
    port: int
    name: str
    user:str
    password: SecretStr


class DefaultSettings(BaseModel):
    secret: SecretStr
    algorithm: str


class AppSettings(BaseSettings):
    database: DatabaseSettings
    default: DefaultSettings


    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )
