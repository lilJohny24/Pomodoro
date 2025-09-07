from dataclasses import dataclass

from jose import jwt
from typing import Optional
from datetime import datetime, timezone, timedelta

from app.users.auth.client import GoogleClient, YandexClient, MailClient
from app.exception import TokenExpired, TokenNotCorrect, UserNotFoundException, UserNotCorrectPasswordException
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.schema import UserCreateSchema, UserLoginSchema
from app.users.user_profile.models import UserProfile
from app.settings import Settings  # Добавлен импорт модели

@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient 
    yandex_client: YandexClient
    mail_client: MailClient

    async def google_auth(self, code: str):
        user_data = await self.google_client.get_user_info(code=code)
        if user := await self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        
        create_user_data = UserCreateSchema(google_access_token=user_data.access_token, email=user_data.email, name=user_data.name)
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)

        self.mail_client.send_welcome_email(to=user_data.email)

        return UserLoginSchema(user_id=created_user.id, access_token=access_token)
    

    async def yandex_auth(self, code: str):
        user_data = self.yandex_client.get_user_info(code=code)

        if user := await self.user_repository.get_user_by_email(email=user_data.default_email):
            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        
        create_user_data = UserCreateSchema(yandex_access_token=user_data.access_token, email=user_data.default_email, name=user_data.name)
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = self.generate_access_token(user_id=created_user.id)

        self.mail_client.send_welcome_email(to=user_data.email)

        return UserLoginSchema(user_id=created_user.id, access_token=access_token)


    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url   

    def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url
    
    def get_yandex_auth(self, code: str):
        pass

    async def login(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.get_user_by_username(username)
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
        expires_date_unix = (datetime.now(tz=timezone.utc) + timedelta(days=7)).timestamp()

        token = jwt.encode({'user_id': user_id, 'expire': expires_date_unix}, self.settings.JWT_SECRET_KEY, self.settings.JWT_ENCODE_ALGORITHM)   

        return token
    

    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, key = self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ENCODE_ALGORITHM])
        except:
            raise TokenNotCorrect
        if payload['expire'] < datetime.now(tz=timezone.utc).timestamp():
            raise TokenExpired
        return payload['user_id']