from fastapi import APIRouter, status, HTTPException, Depends
from typing import List, Annotated
from dependecy import get_tasks_repository, get_tasks_cache_repostiory, get_task_service
from repository import TaskRepository, TaskCache 
from fixtures import tasks as fixtures_tasks
from schema.task import TaskSchema

from database.database import get_db_session
from service.task import TaskService

router = APIRouter(prefix='/task', tags=["task"])

@router.get(
    "/all",
    response_model=List[TaskSchema],
    #response_model_exclude_unset=True,
    summary="Get all tasks",
    description="Returns a list of all tasks"
)
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)]
):
    return task_service.get_tasks()
    


@router.post(
    "/",
    response_model=TaskSchema,
    #response_model_exclude_unset=True,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Adds a new task to the list"
)
async def create_task(
    task: TaskSchema,
    task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]
    ):
    task_id = task_repository.create_task(task)
    task.id = task_id
    return task

@router.patch(
    "/{task_id}",
    response_model=TaskSchema,
    summary="Update task name",
    description="Updates the name of a specific task"
)
async def patch_task(task_id: int, name: str, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)], ):
    return task_repository.update_task_name(task_id, name)
    
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Removes a task from the list"
)
async def delete_task(task_id: int, task_repository: Annotated[TaskRepository, Depends(get_tasks_repository)]):
    task_repository.delete_task(task_id)
    return {'message': 'task deleted successfully'}
    