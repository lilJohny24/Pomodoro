from dataclasses import dataclass
from typing import Optional

from exception import UserNotFoundException, UserNotCorrectPasswordException
from repository.user import UserRepository
from schema.user import UserLoginSchema
from models.user import UserProfile  # Добавлен импорт модели

@dataclass
class AuthService:
    user_repository: UserRepository

    def login(self, username: str, password: str) -> UserLoginSchema:
        user = self.user_repository.get_user_by_username(username)
        self._validate_auth_user(user, password)
        return UserLoginSchema(
            user_id=user.id,
            access_token=user.access_token
        )
    
    @staticmethod
    def _validate_auth_user(user: Optional[UserProfile], password: str):
        if user is None:
            raise UserNotFoundException()
        if user.password != password:
            raise UserNotCorrectPasswordException()