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

    @classmethod
    async def getAll(self, limit: int = 100, skip: int = 0):
        return await self.model.all().offset(skip).limit(limit)

    @abstractmethod
    async def findOne(self, *args, **kwargs):
        pass

    @abstractmethod
    async def create(self, **payload):
        return await self.model.create(**payload)

    @abstractmethod
    async def update(self, id: int, *args, **kwargs):
        pass

    @abstractmethod
    async def remove(self, id: int):
        pass