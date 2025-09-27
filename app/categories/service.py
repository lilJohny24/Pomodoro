from dataclasses import dataclass
from app.categories.repository.category import CategoryRepository
from app.categories.schema import CategoryCreateSchema, CategorySchema

@dataclass
class CategoryService:
    category_repository: CategoryRepository

    async def get_categories(self) -> list[CategorySchema]:
        categories = await self.category_repository.get_categories()
        return [CategorySchema.from_orm(category) for category in categories]  # Конвертируем в схему
    
    async def create_category(self, body: CategoryCreateSchema) -> CategorySchema:
        category_id = await self.category_repository.create_category(body)
        # Получаем созданную категорию для возврата полного объекта
        category = await self.category_repository.get_category(category_id)
        return CategorySchema.from_orm(category)  # Конвертируем в схему
    
    async def update_category_name(self, category_id: int, name: str) -> CategorySchema:
        category = await self.category_repository.get_category(category_id=category_id)
        if not category:
            raise 'Error'
        category = await self.category_repository.update_category_name(category_id=category_id, name=name)
        return CategorySchema.from_orm(category)  # Конвертируем в схему

    async def delete_category(self, category_id: int) -> None:
        await self.category_repository.delete_category(category_id=category_id)