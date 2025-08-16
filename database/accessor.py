from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from settings import Settings

settings = Settings()

engine = create_engine(settings.db_url, echo=True)  # echo=True = лог SQL
SessionLocal = sessionmaker(bind=engine)

def get_db_session() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("DB URL:", settings.db_url)
