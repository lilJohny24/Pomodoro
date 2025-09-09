from unittest.mock import AsyncMock, MagicMock
import httpx
import pytest
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from app.settings import Settings
from app.users.auth.client.google import GoogleClient
from app.users.auth.client.yandex import YandexClient
from app.users.auth.schema import YandexUserData, GoogleUserData
from tests.fixtures.users.user_model import EXISTS_GOOGLE_USER_ID, EXISTS_GOOGLE_USER_EMAIL

faker = FakerFactory.create()
settings = Settings()
async_client: httpx.AsyncClient

@pytest.fixture
def google_user_info_data() -> GoogleUserData:
    return GoogleUserData(
        id=faker.random_int(),
        email=EXISTS_GOOGLE_USER_EMAIL,
        name=faker.name(),
        verified_email=True,
        access_token=faker.sha256()
    )

@pytest.fixture
def yandex_user_info_data() -> dict:
    return YandexUserData(
        id=faker.random_int(),
        default_email=faker.email(),
        login=faker.name(),
        access_token=faker.sha256(),
        real_name=faker.name())




@pytest.fixture
def yandex_client():
    from app.users.auth.client import YandexClient
    from app.settings import Settings
    import httpx
    
    client = YandexClient(
        settings=Settings(),
        async_client=MagicMock(spec=httpx.AsyncClient)
    )
    
    # ЗАМЕНИТЕ MagicMock на реальные значения:
    client.get_user_info = AsyncMock(return_value=type('obj', (object,), {
        'default_email': faker.email(),
        'name': faker.name(),
        'access_token': faker.sha256()
    })())
    
    return client



@pytest.fixture
async def async_client():
    async with httpx.AsyncClient() as client:
        yield client

@pytest.fixture
def google_client():
    from app.users.auth.client import GoogleClient
    from app.settings import Settings
    import httpx
    
    client = GoogleClient(
        settings=Settings(),
        async_client=MagicMock(spec=httpx.AsyncClient)
    )
    
    # Просто придумайте тестовые данные:
    client.get_user_info = AsyncMock(return_value=type('obj', (object,), {
        'email': faker.email(),              # 👈 случайный email
        'name': faker.name(),                # 👈 случайное имя
        'access_token': faker.sha256(),      # 👈 случайный токен
        'verified_email': True,
        'id': faker.random_int()
    })())
    return client