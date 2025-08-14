from fastapi import FastAPI
from handlers import routers  # Импорт всех роутеров


app = FastAPI()

for router in routers:
    app.include_router(router)  # Подключение всех роутеров