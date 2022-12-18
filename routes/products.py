from fastapi import APIRouter, Depends
from schemas import products, user
from repositories.products import ProductRepository, SaveProductRepository
from database.helpers import get_current_user

router = APIRouter()

@router.post(path='/')
async def save(credentials: products.ProductRegisterSchema, repo: SaveProductRepository = Depends(), user: user.UserSchema = Depends(get_current_user)):
    """Save new product"""
    return await repo.register(credentials, user)

@router.get(path='/')
async def get_products(repo: ProductRepository = Depends()):
    return await repo.getAll()

@router.get(path='/{title}')
async def get_product_by_name(title: str, repo: ProductRepository = Depends()):
    return await repo.findOne(title)

@router.get(path='/category/{name}')
async def get_product_by_category(name: str, repo: ProductRepository = Depends()):
    return await repo.filter_by_category(name)

