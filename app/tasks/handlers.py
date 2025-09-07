import asyncio
import time
from fastapi import APIRouter, status, HTTPException, Depends, BackgroundTasks
from typing import List, Annotated
from app.dependency import get_tasks_repository, get_task_service, get_request_user_id
from app.exception import TaskNotFound
from app.tasks.repository import TaskRepository, TaskCache 
#from fixtures import tasks as fixtures_tasks
from app.tasks.schema import TaskCreateSchema, TaskSchema

#from infrastructure.database import get_db_session
from app.tasks.service import TaskService

router = APIRouter(prefix='/task', tags=["task"])


async def get_tasks_log(tasks_count: int):
    await asyncio.sleep(3)
    print(f'get {tasks_count} tasks')


@router.get(
    "/all",
    response_model=List[TaskSchema],
    summary="Get all tasks",
    description="Returns a list of all tasks"
)
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
    background_tasks: BackgroundTasks
):
    
    tasks = await task_service.get_tasks()  # ✅ Правильно - есть await
    background_tasks.add_task(get_tasks_log, tasks_count=len(tasks))
    return tasks 

@router.post(
    "/",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Adds a new task to the list"
)
async def create_task(
    body: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
    user_id: int = Depends(get_request_user_id)
):
    task = await task_service.create_task(body, user_id)  # ✅ Добавлен await
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskSchema,
    summary="Update task name",
    description="Updates the name of a specific task"
)
async def patch_task(
    task_id: int, 
    name: str, 
    task_service: Annotated[TaskService, Depends(get_task_service)], 
    user_id: int = Depends(get_request_user_id)
):
    try:
        return await task_service.update_task_name(task_id=task_id, name=name, user_id=user_id)  # ✅ Добавлен await
    except TaskNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Removes a task from the list"
)
async def delete_task(
    task_id: int, 
    task_service: Annotated[TaskService, Depends(get_task_service)], 
    user_id: int = Depends(get_request_user_id)
):
    try:
        await task_service.delete_task(task_id=task_id, user_id=user_id)  # ✅ Добавлен await
    except TaskNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )