from fastapi import APIRouter, status, HTTPException
from typing import List

from fixtures import categories as fixtures_categories
from schema.category import Category

router = APIRouter(prefix='/category', tags=["category"])

@router.get(
    "/all",
    response_model=List[Category],
    summary="Get all categories",
    description="Returns a list of all categories"
)
async def get_categories():
    # Конвертируем каждый словарь в Pydantic-модель
    return [Category(**c) for c in fixtures_categories]

@router.post(
    "/",
    response_model=Category,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
    description="Adds a new category to the list"
)
async def create_category(category: Category):
    fixtures_categories.append(category.dict())  # Сохраняем в формате dict
    return category

@router.patch(
    "/{category_id}",
    response_model=Category,
    summary="Update category name",
    description="Updates the name of a specific category"
)
async def patch_category(category_id: int, name: str):
    for category in fixtures_categories:
        if category["id"] == category_id:  # Работаем с dict
            category["name"] = name
            return Category(**category)    # Возвращаем модель
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found"
    )

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a category",
    description="Removes a category from the list"
)
async def delete_category(category_id: int):
    for index, category in enumerate(fixtures_categories):
        if category["id"] == category_id:  # Работаем с dict
            del fixtures_categories[index]
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found"
    )
