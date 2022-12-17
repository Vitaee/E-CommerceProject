from .base import BaseRepository, Repository
from models.products import Business
from datetime import datetime
from schemas import products as schemas


class SaveBusinessRepository(BaseRepository):

    model = Business

    async def register(self, schema: schemas.BusinessRegisterSchema):
        """ Save business """

        business_obj = Business(**schema.dict())
        await business_obj.save()
        
        return await self.serializer.from_tortoise_orm(business_obj)

class BusinessRepository(Repository):

    model = Business

    async def getAll(self, limit: int = 5, skip: int = 0):
        return await Business.all().offset(skip).limit(limit)

    async def findOne(self, name: str):
        return await Business.filter(name__contains=name).first()

    async def create(self, payload: dict):
        return await Business.create(**payload)

    async def update(self, id: int, payload: dict):
        pass

    async def remove(self, id: int):
        return await Business.find(id).delete()