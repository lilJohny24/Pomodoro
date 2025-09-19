import pytest
from unittest.mock import MagicMock, AsyncMock

import pytest_asyncio
#from app.dependency import get_broker_producer, get_broker_consumer
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository
from app.settings import Settings
from app.users.auth.client import MailClient

@pytest.fixture
def mail_client():
    """Мокаем почтовый клиент, чтобы в тестах не улетали реальные письма"""
    mock = MagicMock()
    mock.send_welcome_email = AsyncMock(return_value=None)
    return mock

@pytest.fixture
def real_mail_client(mail_client):  # ← используйте существующую mock фикстуру
    return mail_client  # ЧТОБЫ ИСПОЛЬЗОВАТЬ ТЕСТОВЫЕ ДАННЫЕ НУЖНО ЗАКОМИТИТЬ ЭТУ ФИКСТУРУ И В ФИКСТУРЕ AUTH_SERVICE ИСПОЛЬЗОВАТЬ MAIL_CLIENT 

@pytest.fixture
def mock_auth_service():
    """Заглушка для сервиса аутентификации"""
    return MagicMock()

@pytest_asyncio.fixture
async def auth_service(yandex_client, google_client, mail_client, get_db_session):  # ← измените здесь
    return AuthService(
        user_repository=UserRepository(db_session=get_db_session),
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=mail_client, # ← и здесь менять
        #broker_producer=await get_broker_producer(),
        #broker_consumer=await get_broker_consumer()
    )