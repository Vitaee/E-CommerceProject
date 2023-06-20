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
