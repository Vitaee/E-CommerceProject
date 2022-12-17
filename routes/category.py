from fastapi import APIRouter, Depends
from schemas import products as schemas
from repositories.categories import CategoryRepository, SaveCategoryRepository

router = APIRouter()

@router.post(path='/')
async def save(credentials: schemas.CategoryRegisterSchema, repo: SaveCategoryRepository = Depends()):
    """Save new category"""
    return await repo.register(credentials)

@router.get(path='/')
async def get_categories(repo: CategoryRepository = Depends()):
    return await repo.getAll()


