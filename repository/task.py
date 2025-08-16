from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from models.tasks import Category, TaskSchema

class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self):
        return self.db_session.execute(select(TaskSchema)).scalars().all()

    def get_task(self, task_id: int) -> TaskSchema | None:
        return (
            self.db_session
            .execute(select(TaskSchema).where(TaskSchema.id == task_id))
            .scalar_one_or_none()
        )
        
    def create_task(self, task: TaskSchema) -> int:
        task_model = TaskSchema(**task.dict())
        self.db_session.add(task_model)
        self.db_session.commit()
        self.db_session.refresh(task_model)
        return task_model.id

    def delete_task(self, task_id: int) -> None:
        query = delete(TaskSchema).where(TaskSchema.id == task_id)
        self.db_session.execute(query)
        self.db_session.commit()

    def get_task_by_category_name(self, category_name: str) -> list[TaskSchema] | None:
        query = (
            select(TaskSchema)
            .join(Category, TaskSchema.category_id == Category.id)
            .where(Category.name == category_name)
        )
        return self.db_session.execute(query).scalars().all()
        
    def update_task_name(self, task_id: int, name: str) -> TaskSchema | None:
        query = (
            update(TaskSchema)
            .where(TaskSchema.id == task_id)
            .values(name=name)
            .returning(TaskSchema)
        )
        task = self.db_session.execute(query).scalar_one_or_none()
        self.db_session.commit()
        return task
