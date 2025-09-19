import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.dependency import get_broker_consumer
from app.tasks.handlers import router as tasks_router
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_router




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запускаем потребление сообщений в фоне, а не блокируем startup
    broker_consumer = await get_broker_consumer()
    
    # Создаем фоновую задачу
    task = asyncio.create_task(broker_consumer.consume_callback_message())
    
    yield
    
    # Отменяем задачу при shutdown
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(user_router)