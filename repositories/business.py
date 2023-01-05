from .base import BaseRepository, Repository
from models.products import Business
from datetime import datetime
from schemas import products as schemas


class SaveBusinessRepository(BaseRepository):

    model = Business

    async def register(self, schema: schemas.BusinessRegisterSchema, user):
        """ Save business """

        business_obj = Business(**schema.dict())
        business_obj.business_owner = user
        await business_obj.save()
        
        return await self.serializer.from_tortoise_orm(business_obj)

class BusinessRepository(Repository):

    model = Business

    async def getAll(self, limit: int = 5, skip: int = 0):
        return await self.model.all().offset(skip).limit(limit)

    async def findOne(self, name: str):
        return await self.model.filter(name__contains=name).first()

    async def create(self, payload: dict):
        return await self.model.create(**payload)

    async def update(self, id: int, payload: dict):
        pass

    async def remove(self, id: int):
        return await self.model.find(id).delete()