from pydantic.main import BaseModel
from pydantic import EmailStr, SecretStr
from pydantic.main import BaseModel


class AdminLoginModel(BaseModel):
    username: str | EmailStr
    password: SecretStr


class CreateUserModel(BaseModel):
    username: str
    fullname: str
    address: str
    phone_number: str
    opening_balance: float

    
class ListUserParams(BaseModel):
    page_number: int | None = None
    page_size: int | None = None
    user_id: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
