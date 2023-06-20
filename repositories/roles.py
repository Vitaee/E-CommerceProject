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