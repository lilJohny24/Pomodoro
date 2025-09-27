from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.categories.models import Category
from app.categories.schema import CategoryCreateSchema



class CategoryRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_categories(self):
        result = await self.db_session.execute(select(Category))
        return result.scalars().all()

    async def get_category(self, category_id: int) -> Category | None:  
        result = await self.db_session.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()
    
    async def create_category(self, category: CategoryCreateSchema) -> int:
        category_model = Category(name=category.name, type=category.type)
        self.db_session.add(category_model)
        await self.db_session.commit()
        await self.db_session.refresh(category_model)
        return category_model.id
    
    async def delete_category(self, category_id: int) -> None:
        query = delete(Category).where(Category.id == category_id)
        await self.db_session.execute(query)
        await self.db_session.commit()
    
    async def update_category_name(self, category_id: int, name: str) -> Category | None:
        query = update(Category).where(Category.id == category_id).values(name=name).returning(Category)
        result = await self.db_session.execute(query)
        category = result.scalar_one_or_none()
        await self.db_session.commit()
        return category