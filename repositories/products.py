from .base import BaseRepository, Repository
from models.products import Product, Business, Category
from datetime import datetime
from schemas import products as schemas


class SaveProductRepository(BaseRepository):

    model = Product

    async def register(self, schema: schemas.ProductRegisterSchema) -> Product:
        """ Save product """
        product_obj = Product(**schema.dict())
        await product_obj.save()
        return await self.serializer.from_tortoise_orm(product_obj)

class ProductRepository(Repository):

    model = Product

    async def getAll(self, limit: int = 100, skip: int = 0):
        return await Product.all().offset(skip).limit(limit)

    async def findOne(self, id: int):
        return await Product.filter(id=id).first()

    async def create(self, payload: dict):
        return await Product.create(**payload)

    async def update(self, id: int, payload: dict):
        user = await Product.find(id)
        await user.update_from_dict(payload)
        await user.save()
        return user

    async def remove(self, id: int):
        return await Product.find(id).delete()