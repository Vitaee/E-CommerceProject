from .base import BaseRepository, Repository
from models.products import Category
from datetime import datetime
from schemas import products as schemas


class SaveCategoryRepository(BaseRepository):

    model = Category

    async def register(self, schema: schemas.CategoryRegisterSchema):
        """ Save category """

        category_obj = Category(**schema.dict())
        await category_obj.save()
        
        return await self.serializer.from_tortoise_orm(category_obj)

class CategoryRepository(Repository):

    model = Category

    async def create(self, payload: dict):
        return await Category.create(**payload)

    async def update(self, id: int, payload: dict):
        pass

    async def remove(self, id: int):
        return await Category.find(id).delete()