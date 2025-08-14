from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from database import TaskSchema, Category, get_db_session  # Убедитесь, что Tasks и get_db_session существуют



class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self):
        with self.db_session() as session:
            task: list[TaskSchema] = session.execute(select(TaskSchema)).scalars().all()
            return task

    def get_task(self, task_id: int) -> TaskSchema | None:
        with self.db_session() as session:
            task: TaskSchema = session.execute(select(TaskSchema).where(TaskSchema.id == task_id)).scalar_one_or_none()
            return task
        
    def create_task(self, task: TaskSchema) -> int:
        task_model = TaskSchema(**task.dict())
        with self.db_session() as session:
            session.add(task_model)
            session.commit()
            session.refresh(task_model)
        return task_model.id

    def delete_task(self, task_id: int) -> TaskSchema | None:
        query = delete(TaskSchema).where(TaskSchema.id == task_id)
        with self.db_session() as session:
            session.execute(query)
            session.commit()

    def get_task_by_category_name(self, category_name:str) -> list[TaskSchema] | None:
        query = select(TaskSchema).join(Category, TaskSchema.category_id == Category.id).where(Category.name == category_name)
        with self.db_session() as session:
            task: list[TaskSchema] = session.execute(query).scalars().all()
            return task
        
    def update_task_name(self, task_id: int, name: str) -> TaskSchema | None:
        with self.db_session() as session:
            query = (
                update(TaskSchema)
                .where(TaskSchema.id == task_id)
                .values(name=name)
                .returning(TaskSchema)
            )
            task = session.execute(query).scalar_one_or_none()
            session.commit()
            return task


