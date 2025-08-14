from redis import Redis
from schema.task import TaskSchema
class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> list[TaskSchema]:
        with self.redis as redis:
            task_json = redis.lrange('tasks', 0, -1)
            return [TaskSchema.model_validate_json(task.decode('utf-8')) for task in task_json]

    def set_tasks(self, tasks: list[TaskSchema]):
        tasks_json = [task.json() for task in tasks]
        with self.redis as redis:
           redis.lpush('tasks', *tasks_json)