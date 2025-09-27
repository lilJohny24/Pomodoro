import asyncio
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from app.categories.models import Category
from app.categories.schema import CategoryCreateSchema, CategorySchema
from app.categories.service import CategoryService
from app.dependency import get_category_service


router = APIRouter(prefix='/category', tags=['category'])

async def get_categories_log(category_count: int):
    await asyncio.sleep(3)
    print(f'get {category_count} categories')

@router.get(
    '/all',
    response_model=List[CategorySchema],
    summary='Get all categories',
    description='Returns a list of all categories'
)
async def get_categories(
    category_service: Annotated[CategoryService, Depends(get_category_service)]


):
    categories = await category_service.get_categories()
    return categories


@router.post(
    "/",
    response_model=CategorySchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
    description="Adds a new category to the list"
)
async def create_task(
    body: CategoryCreateSchema,
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    category = await category_service.create_category(body)  # ✅ Добавлен await
    return category


@router.patch("/{category_id}")  # измените на category_id
async def patch_category(
    name: str,
    category_id: int,  # принимаем ID вместо name
    category_service: Annotated[CategoryService, Depends(get_category_service)], 
):
    try:
        return await category_service.update_category_name(category_id=category_id, name=name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{category_id}")  # измените на category_id
async def delete_task(
    category_id: int,  # принимаем ID вместо name
    category_service: Annotated[CategoryService, Depends(get_category_service)], 
):
    try:
        await category_service.delete_category(category_id=category_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))