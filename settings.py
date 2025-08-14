from pydantic import BaseModel  # Используем BaseModel вместо BaseSettings для простоты

class Settings(BaseModel):
    DB_HOST: str = 'db'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_NAME: str = 'pomodoro'
    CACHE_HOST: str = '0.0.0.0'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    
    