from dataclasses import dataclass


from repository.user import UserRepository
from schema.user import UserLoginSchema
from service.auth import AuthService

@dataclass
class UserService:
    user_repository: 'UserRepository'
    auth_service: 'AuthService'


    def create_user(self, username: str, password: str) -> 'UserLoginSchema':
        user = self.user_repository.create_user(
            username=username,
            password=password
        )
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return {
            "user_id": str(user.id),
            "access_token": access_token
        }

    