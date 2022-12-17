from .base import BaseRepository, Repository
from models.products import Product, Business, Category
from datetime import datetime
from schemas import products as schemas


class SaveProductRepository(BaseRepository):

    model = Product

    async def register(self, schema: schemas.ProductRegisterSchema):
        """ Save product """
        get_category_obj = await Category.filter(name=schema.category).first()
        get_business_obj = await Business.filter(name=schema.business).first()
        

        product_obj = Product(**schema.dict(exclude={'category', 'business'}))
        await product_obj.save()
        
        await product_obj.business.add(get_business_obj)
        await product_obj.category.add(get_category_obj)
        
        
        return await self.serializer.from_tortoise_orm(product_obj)

class ProductRepository(Repository):

    model = Product

    async def getAll(self, limit: int = 5, skip: int = 0):
        d = await Product.get(title="Macbook Pro")
        c = await d.category.all()
        for i in c:
            print("\n\n\n\n\n",i.name, "\n\n\n\n\n")

            
        return await Product.all().offset(skip).limit(limit)

    async def findOne(self, title: str):
        return await Product.filter(title__contains=title).first()

    async def filter_by_category(self, name: str):
        return await Product.filter(category__name=name).first()

    async def create(self, payload: dict):
        return await Product.create(**payload)

    async def update(self, id: int, payload: dict):
        product = await Product.find(id)
        await product.update_from_dict(payload)
        await product.save()
        return product

    async def remove(self, id: int):
        return await Product.find(id).delete()