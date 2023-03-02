from .base import BaseRepository, Repository
from models.users import  Role
from schemas import user as schemas


class SaveRoleRepository(BaseRepository):

    model = Role

    async def register(self, schema: schemas.RoleInSchema):
        """Save role data"""
        role_obj = self.model(**schema.dict())
        await role_obj.save()
        return await self.serializer.from_tortoise_orm(role_obj)

class RoleRepository(Repository):

    model = Role

    async def findOne(self, name: str):
        return await self.model.filter(name=name).first()

    async def create(self, payload: dict):
        return await self.model.create(**payload)

    async def update(self, id: int, payload: dict):
        role = await self.model.get(id=id)
        await role.update_from_dict(payload)
        await role.save()
        return role


    async def remove(self, name: str):
        return await self.model.get(name=name).delete()