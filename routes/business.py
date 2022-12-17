from fastapi import APIRouter, Depends
from schemas import products as schemas
from repositories.business import BusinessRepository, SaveBusinessRepository 

router = APIRouter()

@router.post(path='/')
async def save(credentials: schemas.BusinessRegisterSchema, repo: SaveBusinessRepository = Depends()):
    """Save new business"""
    return await repo.register(credentials)

@router.get(path='/')
async def get_business(repo: BusinessRepository = Depends()):
    return await repo.getAll()


