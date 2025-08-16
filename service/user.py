from dataclasses import dataclass
import secrets
import string

from repository.user import UserRepository
from schema.user import UserLoginSchema

@dataclass
class UserService:
    user_repository: 'UserRepository'

    def create_user(self, username: str, password: str) -> 'UserLoginSchema':
        access_token = self._generate_access_token()
        user = self.user_repository.create_user(
            username=username,
            password=password,
            access_token=access_token
        )
        return {
            "user_id": str(user.id),
            "access_token": user.access_token
        }

    @staticmethod
    def _generate_access_token(length=32) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))