from dataclasses import dataclass  # Добавьте этот импорт

from repository import TaskRepository, TaskCache
from schema.task import TaskSchema

@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    def get_tasks(self) -> list[TaskSchema]:
        if tasks := self.task_cache.get_tasks():
            return tasks
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [TaskSchema.model_validate(task, from_attributes=True) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema
