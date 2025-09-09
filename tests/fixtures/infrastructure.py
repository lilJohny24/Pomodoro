import pytest
import pytest_asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.settings import Settings
from app.infrastructure.database.database import Base


@pytest.fixture
def settings():
    return Settings()


engine = create_async_engine(url="postgresql+asyncpg://postgres:password@db:5432/pomodoro", future=True, echo=True, pool_pre_ping=True)


AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)



@pytest_asyncio.fixture(autouse=True, scope="function")
async def init_models(event_loop):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        tables = ", ".join([f"\"{table.name}\"" for table in Base.metadata.sorted_tables])
        await conn.execute(text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE;"))



@pytest_asyncio.fixture(scope="function")
async def get_db_session():
    # Убираем внутреннюю функцию, возвращаем сразу сессию
    async with AsyncSessionFactory() as session:
        yield session