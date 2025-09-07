from pydantic import BaseModel  # Используем BaseModel вместо BaseSettings для простоты

class Settings(BaseModel):
    DB_HOST: str = 'db'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_DRIVER: str = 'postgresql+asyncpg'
    DB_NAME: str = 'pomodoro'
    CACHE_HOST: str = 'cache'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    JWT_SECRET_KEY: str = 'secret_key' 
    JWT_ENCODE_ALGORITHM: str = 'HS256'
    GOOGLE_CLIENT_ID: str = '502239718197-n7c12nkk2vpqskleiqfihlg3n9g9uin2.apps.googleusercontent.com'
    GOOGLE_SECRET_KEY: str = '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'
    GOOGLE_REDIRECT_URI: str = 'http://localhost:8000/auth/google'
    GOOGLE_TOKEN_URL: str = 'https://accounts.google.com/o/oauth2/token'
    YANDEX_CLIENT_ID: str = 'da30003703444a60b5abc10bcf3338a1'
    YANDEX_CLIENT_SECRET: str = '3f3366cf7cb645fb94d8eb874ccd365d'
    YANDEX_REDIRECT_URI: str = 'http://localhost:8000/auth/yandex'
    YANDEX_TOKEN_URL: str = 'https://oauth.yandex.ru/token'
    CELERY_REDIS_URL: str = 'redis://localhost:6379'
    FROM_EMAIL: str = 'johnvbg2008@gmail.com'
    SMTP_HOST: str = 'smtp.gmail.com'
    SMTP_PORT: int = 465
    SMPT_PASSWORD: str = 'Qazxswedc20080906'
    

    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    @property
    def google_redirect_url(self) -> str:
        return f'https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline'
    
    @property
    def yandex_redirect_url(self) -> str:
        return f'https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&redirect_uri={self.YANDEX_REDIRECT_URI}'