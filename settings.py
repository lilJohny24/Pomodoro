from pydantic import BaseModel  # Используем BaseModel вместо BaseSettings для простоты

class Settings(BaseModel):
    sqlite_db_name: str = 'pomodoro.sqlite'