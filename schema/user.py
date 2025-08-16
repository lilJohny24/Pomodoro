from pydantic import BaseModel

class UserLoginSchema(BaseModel):
    user_id: int  # Изменил str на int
    access_token: str

class UserCreateSchema(BaseModel):
    username: str
    password: str