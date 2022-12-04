from .base import BaseRepository, Repository
from models.users import User, VerifyCode
from core.security import hash_password, create_access_token
from core.exceptions import (
    BadCredentialsError,
    TokenExpirateError
)
from datetime import datetime
from core.settings import TIMEZONE
from database.helpers import authenticate
from schemas import user as schemas
from tasks.users import send_confirmation_email


class AuthRepository(BaseRepository):

    model = User

    async def register(self, schema: schemas.RegisterSchema) -> User:
        """ Registration user """
        user_obj = User(**schema.dict(exclude={'password2'}))
        user_obj.password = hash_password(user_obj.password)
        await user_obj.save()
        send_confirmation_email.delay(user_obj.email)
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

    async def confirm_email(self, schema: schemas.ConfirmEmailSchema) -> User:
        """ User email confirmation """
        confirmer = await VerifyCode.filter(**schema.dict()).first()
        if confirmer:
            diff_date = datetime.now() - confirmer.created_at.replace(
                tzinfo=TIMEZONE
            )
            if diff_date.total_seconds() > 86400:
                raise TokenExpirateError(
                    'Your confirmation token is expirated.')
        else:
            raise BadCredentialsError('corrupted credentials.')
        user = await User.filter(email=schema.email).first()
        if user is None:
            raise 'No user found with email.'
        user.email_confirmed_at = datetime.now()
        user.updated_at = datetime.now()
        await user.save()
        return await self.serializer.from_tortoise_orm(user)

class UserRepository(Repository):

    model = User

    async def getAll(self, limit: int = 100, skip: int = 0):
        return await User.all().offset(skip).limit(limit)

    async def findOne(self, id: int):
        return await User.filter(id=id).first()

    async def create(self, payload: dict):
        return await User.create(**payload)

    async def update(self, id: int, payload: dict):
        user = await User.find(id)
        await user.update_from_dict(payload)
        await user.save()
        return user


    async def remove(self, id: int):
        return await User.find(id).delete()