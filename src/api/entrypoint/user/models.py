from pydantic import BaseModel, SecretStr


class UserLoginModel(BaseModel):
    username: str
    password: SecretStr


class Amount(BaseModel):
    amount: float
