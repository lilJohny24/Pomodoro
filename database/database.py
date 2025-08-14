from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Попробуйте явно указать кодировку в URL:
engine = create_engine('postgresql+psycopg2://postgres:password@db:5432/pomodoro')


Session = sessionmaker(engine)

def get_db_session() -> Session:
    return Session