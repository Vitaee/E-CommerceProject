from fastapi import APIRouter, Depends
from database.helpers import get_current_user
from schemas import user as schemas
from repositories.user import UserRepository

router = APIRouter()

@router.get(path='/{other_username}/')
async def get_other_user(other_username:str, repo: UserRepository = Depends(), current_user: schemas.UserSchema = Depends(get_current_user)):
    """Get other user"""
    return await repo.findOne(other_username)

@router.put(path='/')
async def update_user_credentials(payload: schemas.UserUpdateSchema, repo: UserRepository = Depends(), current_user: schemas.UserSchema = Depends(get_current_user)):
    """Update user information"""
    return await repo.update(current_user.id, payload.dict())

@router.delete(path='/')
async def delete_user_account(repo: UserRepository = Depends(), current_user: schemas.UserSchema = Depends(get_current_user)):
    "Delete user account"
    return await repo.remove(current_user.id)