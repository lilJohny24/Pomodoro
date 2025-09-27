import asyncio
import json
from typing import Annotated
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import Depends, HTTPException, Request, Security, security
import httpx
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.broker.consumer import BrokerConsumer
from app.broker.producer import BrokerProducer
from app.categories.repository.category import CategoryRepository
from app.categories.service import CategoryService
from app.users.auth.client import GoogleClient
from app.users.auth.client import YandexClient
from app.exception import TokenExpired, TokenNotCorrect
from app.tasks.repository import TaskRepository, TaskCache
from app.infrastructure.database import get_db_session
from app.infrastructure.cache import get_redis_connection
from app.users.auth.client.mail import MailClient
from app.users.user_profile.repository import UserRepository
from app.tasks.service import TaskService
from app.users.user_profile.service import UserService
from app.users.auth.service import AuthService
from app.settings import Settings

    
# Убрали event_loop, так как он не нужен для AIOKafka в современных версиях

async def get_broker_producer() -> BrokerProducer:
    settings = Settings()
    return BrokerProducer(
        producer=AIOKafkaProducer(
            bootstrap_servers=settings.BROKER_URL,
            # Убрали loop параметр
        ),
        email_topic=settings.EMAIL_TOPIC
    )


async def get_broker_consumer() -> BrokerConsumer:
    settings = Settings()
    return BrokerConsumer(
        consumer=AIOKafkaConsumer(
            settings.EMAIL_CALLBACK_TOPIC,
            bootstrap_servers=settings.BROKER_URL,
            value_deserializer=lambda message: json.loads(message.decode('utf-8'))
        ),
        email_callback_topic=settings.EMAIL_CALLBACK_TOPIC
    )


async def get_mail_client(
    broker_producer: Annotated[BrokerProducer, Depends(get_broker_producer)],
    broker_consumer: Annotated[BrokerConsumer, Depends(get_broker_consumer)]
) -> MailClient:
    return MailClient(
        settings=Settings(), 
        broker_producer=broker_producer, 
        broker_consumer=broker_consumer
    )


async def get_categories_repository(db_session: AsyncSession = Depends(get_db_session)) -> CategoryRepository:
    return CategoryRepository(db_session)


async def get_tasks_repository(db_session: AsyncSession = Depends(get_db_session)) -> TaskRepository:
    return TaskRepository(db_session)


async def get_tasks_cache_repostiory() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)


async def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        task_cache: TaskCache = Depends(get_tasks_cache_repostiory)
) -> TaskService:
    return TaskService(
        task_repository=task_repository,
        task_cache=task_cache
    )


async def get_category_service(
        category_repository: CategoryRepository = Depends(get_categories_repository)
) -> CategoryService:
    return CategoryService(
        category_repository=category_repository
    )



async def get_user_repository(db: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db)


# Убрали get_async_client, так как он больше не нужен

async def get_google_client() -> GoogleClient:
    return GoogleClient(settings=Settings())  # Убрали async_client параметр

async def get_yandex_client() -> YandexClient:
    return YandexClient(settings=Settings())  # Убрали async_client параметр


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository), 
    google_client: GoogleClient = Depends(get_google_client), 
    yandex_client: YandexClient = Depends(get_yandex_client), 
    mail_client: MailClient = Depends(get_mail_client)
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=Settings(), 
        google_client=google_client,  
        yandex_client=yandex_client, 
        mail_client=mail_client
    )


async def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository),   
    auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(user_repository=user_repo, auth_service=auth_service)



reusable_oauth2 = security.HTTPBearer()

async def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service), 
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2)
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)
    except TokenExpired as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    except TokenNotCorrect as e:
        raise HTTPException(
            status_code=401,
            detail=e.detail
        )
    return user_id