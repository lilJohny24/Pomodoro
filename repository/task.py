from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from models.tasks import Category, TaskSchema
from schema.task import TaskCreateSchema

class TaskRepository:
    def __init__(self, db_session: AsyncSession):  # Изменено на AsyncSession
        self.db_session = db_session

    async def get_tasks(self):  # Добавлен async
        result = await self.db_session.execute(select(TaskSchema))
        return result.scalars().all()
    

    async def get_user_task(self, task_id: int, user_id: int) -> TaskSchema:  # Добавлен async
        query = select(TaskSchema).where(TaskSchema.id == task_id, TaskSchema.user_id == user_id)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def get_task(self, task_id: int) -> TaskSchema | None:  # Добавлен async
        result = await self.db_session.execute(select(TaskSchema).where(TaskSchema.id == task_id))
        return result.scalar_one_or_none()
    
        
    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:  # Добавлен async
        task_model = TaskSchema(name=task.name, pomodoro_count=task.pomodoro_count, category_id=task.category_id, user_id=user_id)
        self.db_session.add(task_model)
        await self.db_session.commit()
        await self.db_session.refresh(task_model)
        return task_model.id

    async def delete_task(self, task_id: int, user_id: int) -> None:  # Добавлен async
        query = delete(TaskSchema).where(TaskSchema.id == task_id, TaskSchema.user_id == user_id)
        await self.db_session.execute(query)
        await self.db_session.commit()

    async def get_task_by_category_name(self, category_name: str) -> list[TaskSchema] | None:  # Добавлен async
        query = (
            select(TaskSchema)
            .join(Category, TaskSchema.category_id == Category.id)
            .where(Category.name == category_name)
        )
        result = await self.db_session.execute(query)
        return result.scalars().all()
        
    async def update_task_name(self, task_id: int, name: str) -> TaskSchema | None:  # Добавлен async
        query = (
            update(TaskSchema)
            .where(TaskSchema.id == task_id)
            .values(name=name)
            .returning(TaskSchema)
        )
        result = await self.db_session.execute(query)
        task = result.scalar_one_or_none()
        await self.db_session.commit()
        return task