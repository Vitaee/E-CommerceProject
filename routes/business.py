from fastapi import APIRouter, Depends
from schemas import products, user
from repositories.business import BusinessRepository, SaveBusinessRepository 
from database.helpers import get_current_user

router = APIRouter()

@router.post(path='/')
async def save(credentials: products.BusinessRegisterSchema, repo: SaveBusinessRepository = Depends(), user: user.UserSchema = Depends(get_current_user)):
    """Save new business"""
    return await repo.register(credentials, user)

@router.get(path='/')
async def get_business(repo: BusinessRepository = Depends()):
    return await repo.getAll()


