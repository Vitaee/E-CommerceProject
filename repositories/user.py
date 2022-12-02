from .base import BaseRepository, Repository
from models.users import User, VerifyCode
from core.security import hash_password, create_access_token
from core.exceptions import BadCredentialsError
from database.helpers import authenticate
from schemas import user as schemas


class AuthRepository(BaseRepository):

    model = User

    async def register(self, schema: schemas.RegisterSchema) -> User:
        """ Registration user """
        user_obj = User(**schema.dict(exclude={'password2'}))
        user_obj.password = hash_password(user_obj.password)
        await user_obj.save()
        #send_confirmation_email.delay(user_obj.email)
        return await self.serializer.from_tortoise_orm(user_obj)

    async def login(self, schema: schemas.LoginSchema):
        """ Login user """
        user = await authenticate(
            username=schema.email,
            password=schema.password,
        )
        if not user:
            raise BadCredentialsError('Email or password incorrect.')
        return create_access_token({
            'id': user.id,
            'username': user.username,
            'email': user.email,
        })

class UserRepository(Repository):

    model = User

    async def getAll(self, limit: int = 100, skip: int = 0):
        pass

    async def findOne(self, *args, **kwargs):
        pass

    async def create(self, payload: dict):
        pass

    async def update(self, id: int, payload: dict):
        pass

    async def remove(self, id: int):
        pass