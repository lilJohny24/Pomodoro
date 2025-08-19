from dataclasses import dataclass

from jose import jwt
from typing import Optional
import datetime as dt
from datetime import timedelta

from exception import TokenExpired, TokenNotCorrect, UserNotFoundException, UserNotCorrectPasswordException
from repository.user import UserRepository
from schema.user import UserLoginSchema
from models.user import UserProfile
from settings import Settings  # Добавлен импорт модели

@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        return UserLoginSchema(
            user_id=user.id,
            access_token=access_token
        )
    
    @staticmethod
    def _validate_auth_user(user: Optional[UserProfile], password: str):
        if user is None:
            raise UserNotFoundException()
        if user.password != password:
            raise UserNotCorrectPasswordException()
        

    def generate_access_token(self, user_id: int) -> str:
        expires_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode({'user_id': user_id, 'expire': expires_date_unix}, self.settings.JWT_SECRET_KEY, self.settings.JWT_ENCODE_ALGORITHM)   

        return token
    

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, key = self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except:
            raise TokenNotCorrect
        if payload['expire'] < dt.datetime.utcnow().timestamp():
            raise TokenExpired
        return payload['user_id']