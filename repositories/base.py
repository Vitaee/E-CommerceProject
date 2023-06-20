from abc import ABC, abstractmethod, abstractproperty
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator


class BaseRepository(ABC):

    @abstractproperty
    def model(self):
        pass

    @property
    def serializer(self):
        return pydantic_model_creator(self.model)


class Repository(BaseRepository):

    async def getAll(self, limit: int = 100, skip: int = 0):
        return await self.model.all().offset(skip).limit(limit)
    
    async def findOne(self, name: str):
        return await self.model.filter(name__icontains=name).first()
    
    async def create(self, **payload):
        return await self.model.create(**payload)

    async def update(self, id: int, payload: dict):
        model = await self.model.get(id=id)
        await model.update_from_dict(payload)
        await model.save()
        return model

    async def remove(self, id: int):
        return await self.model.find(id).delete()