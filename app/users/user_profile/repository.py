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
        async with self.db_session as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()
    

    async def create_user(self, user_data: UserCreateSchema) -> UserProfile:
    # Создайте объект модели UserProfile из схемы
        user = UserProfile(
            email=user_data.email,
            name=user_data.name,
            google_access_token=user_data.google_access_token,
            yandex_access_token=user_data.yandex_access_token,
            username=user_data.username,  # если есть
            password=user_data.password   # если есть
        )
        
        async with self.db_session as session:
            session.add(user)  # ✅ Теперь добавляем модель, а не схему
            await session.commit()
            await session.refresh(user)
            return user


    async def get_user(self, user_id) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()
    

    async def get_user_by_username(self, username: str):
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.db_session as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()