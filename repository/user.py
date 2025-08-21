from sqlalchemy import insert, select
from sqlalchemy.orm import Session
#from dataclasses import dataclass
from models import UserProfile
from schema import UserCreateSchema


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session  # Не вызываем как функцию!


    def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email  == email)
        return self.db_session.execute(query).scalar_one_or_none()
    

    def create_user(self, user: UserCreateSchema) -> UserProfile:
        stmt = insert(UserProfile).values(
            **user.model_dump()
        ).returning(UserProfile)
        
        result = self.db_session.execute(stmt)
        self.db_session.commit()
        return result.scalar_one()

    def get_user(self, user_id) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        return self.db_session.execute(query).scalar_one_or_none()
    

    def get_user_by_username(self, username: str):
        query = select(UserProfile).where(UserProfile.username == username)
        return self.db_session.execute(query).scalar_one_or_none()