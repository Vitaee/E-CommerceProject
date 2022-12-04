from fastapi import APIRouter, Depends
from schemas import products as schemas
from repositories.products import ProductRepository, SaveProductRepository

router = APIRouter()

@router.post(path='/product', response_model=schemas.Product)
async def save(credentials: schemas.ProductRegisterSchema, repo: SaveProductRepository = Depends()):
    """Save new product"""
    return await repo.register(credentials)