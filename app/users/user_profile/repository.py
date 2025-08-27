from sqlalchemy import insert, select
from sqlalchemy.orm import Session
#from dataclasses import dataclass
from app.users.user_profile.models import UserProfile
from app.users.user_profile.schema import UserCreateSchema


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session  # Не вызываем как функцию!


    async def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email  == email)
        with self.db_session as session:
            return (await self.db_session.execute(query)).scalar_one_or_none()
    

    async def create_user(self, user: UserCreateSchema) -> UserProfile:
        stmt = insert(UserProfile).values(
            **user.model_dump()
        ).returning(UserProfile)
        
        with self.db_session as session:
            return (await self.db_session.execute(stmt)).scalar()


    async def get_user(self, user_id) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        with self.db_session as session:
            return (await self.db_session.execute(query)).scalar_one_or_none()
    

    async def get_user_by_username(self, username: str):
        query = select(UserProfile).where(UserProfile.username == username)
        with self.db_session as session:
            return (await self.db_session.execute(query)).scalar_one_or_none()