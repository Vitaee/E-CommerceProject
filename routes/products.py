from fastapi import APIRouter, Depends
from schemas import products as schemas
from repositories.products import ProductRepository, SaveProductRepository

router = APIRouter()

@router.post(path='/')
async def save(credentials: schemas.ProductRegisterSchema, repo: SaveProductRepository = Depends()):
    """Save new product"""
    return await repo.register(credentials)

@router.get(path='/')
async def get_products(repo: ProductRepository = Depends()):
    return await repo.getAll()

@router.get(path='/{title}')
async def get_product_by_name(title: str, repo: ProductRepository = Depends()):
    return await repo.findOne(title)

