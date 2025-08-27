from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.database import Base

class TaskSchema(Base):  # Наследуем от Base, а не от DeclarativeBase
    __tablename__ = 'Tasks_table'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    pomodoro_count: Mapped[int] = mapped_column()
    category_id: Mapped[int] = mapped_column()
    user_id : Mapped[int] = mapped_column(ForeignKey('UserProfile.id'), nullable=False)

class Category(Base):
    __tablename__ = 'Categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column() 
    name: Mapped[str] = mapped_column()
    
