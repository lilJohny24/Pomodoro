import pytest
from unittest.mock import MagicMock, AsyncMock
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
def real_mail_client():
    """Реальный почтовый клиент для отправки писем"""
    return MailClient()      # ЧТОБЫ ИСПОЛЬЗОВАТЬ ТЕСТОВЫЕ ДАННЫЕ НУЖНО ЗАКОМИТИТЬ ЭТУ ФИКСТУРУ И В ФИКСТУРЕ AUTH_SERVICE ИСПОЛЬЗОВАТЬ MAIL_CLIENT

@pytest.fixture
def mock_auth_service():
    """Заглушка для сервиса аутентификации"""
    return MagicMock()

@pytest.fixture
def auth_service(yandex_client, google_client, real_mail_client, mail_client, get_db_session):  # ← измените здесь
    return AuthService(
        user_repository=UserRepository(db_session=get_db_session),
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=real_mail_client  # ← и здесь менять
    )