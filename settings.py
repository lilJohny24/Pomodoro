from pydantic import BaseModel  # Используем BaseModel вместо BaseSettings для простоты

class Settings(BaseModel):
    DB_HOST: str = 'db'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_DRIVER: str = 'postgresql+psycopg2'
    DB_NAME: str = 'pomodoro'
    CACHE_HOST: str = '0.0.0.0'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0

    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    