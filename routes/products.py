from fastapi import APIRouter, Depends
from schemas import products, user
from repositories.products import ProductRepository, SaveProductRepository
from database.helpers import get_current_user
from fastapi.responses import JSONResponse
from typing import List
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post(path='/')
async def save(credentials: products.ProductRegisterSchema, repo: SaveProductRepository = Depends(), user: user.UserSchema = Depends(get_current_user)):
    """Save new product"""
    user_role = await user.roles.first()
    if user_role.name == 'user':
        return JSONResponse(content={'message': 'Forbidden!'}, status_code=403)
    return await repo.register(credentials, user)

@router.get(path='/', response_model=List[products.Product])
async def get_products(repo: ProductRepository = Depends()):
    data = await repo.getAll()
    return  jsonable_encoder(data)

@router.get(path='/{title}')
async def get_product_by_name(title: str, repo: ProductRepository = Depends()):
    return await repo.findOne(title)

@router.get(path='/category/{name}')
async def get_product_by_category(name: str, repo: ProductRepository = Depends()):
    return await repo.filter_by_category(name)

