from .base import BaseRepository, Repository
from models.products import Product, Business, Category
from datetime import datetime
from schemas import products as schemas


class SaveProductRepository(BaseRepository):

    model = Product

    async def register(self, schema: schemas.ProductRegisterSchema, user):
        """ Save product """
        get_category_obj = await Category.filter(name=schema.category).first()
        get_business_obj = await Business.filter(business_owner__id=user.id).first()
        

        product_obj = self.model(**schema.dict(exclude={'category'}))
        await product_obj.save()
        
        await product_obj.business.add(get_business_obj)
        await product_obj.category.add(get_category_obj)
        
        
        return await self.serializer.from_tortoise_orm(product_obj)

class ProductRepository(Repository):

    model = Product

    async def filter_by_category(self, name: str):
        return await self.model.filter(category__name=name).first()