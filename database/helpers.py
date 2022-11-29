from fastapi import Depends
from models.users import User
from core.security import JWTBearer, verify_password, decode_token
from jose import ExpiredSignatureError, JWTError
from core.exceptions import (
    TokenExpirateError, TokenInvalidError, UnAuthorizedError,
    BadCredentialsError
)


async def is_authenticated(username: str, password: str) -> bool | User:
    user = await User.get_or_none(email=username)
    if not user:
        return False
    if not verify_password(password):
        return False
    return user


async def authenticate(username: str, password: str) -> User:
    user = await User.get_or_none(email=username)
    if not user:
        raise BadCredentialsError('Email or password incorrect.')
    if not verify_password(password, user.password):
        raise BadCredentialsError('Email or password incorrect.')
    return user


async def get_current_user(token: str = Depends(JWTBearer())):
    try:
        decoded_token = decode_token(token)
        user = await User.get_or_none(id=decoded_token.get('id'))
        if not user:
            raise UnAuthorizedError("Invalid authentication credentials")
        return user
    except ExpiredSignatureError:
        raise TokenExpirateError("Token expired. Get new one")
    except JWTError:
        raise TokenInvalidError("Invalid Token")