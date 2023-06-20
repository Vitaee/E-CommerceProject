from fastapi import APIRouter, Depends
from schemas import  user
from repositories.roles import RoleRepository, SaveRoleRepository
from fastapi.responses import JSONResponse
from typing import List
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post(path='/')
async def save(credentials: user.RoleInSchema, repo: SaveRoleRepository = Depends()):
    """Save new role"""
    # need to check user role.
    #user_role = await user.roles.first()
    #if user_role.name == 'user':
    #    return JSONResponse(content={'message': 'Forbidden!'}, status_code=403)
    return await repo.register(credentials)

@router.get(path='/')
async def get_roles(repo: RoleRepository = Depends()):
    """Get all roles"""
    return await repo.getAll()

@router.put(path='/')
async def update_role(credentials: user.RoleInUpdateSchema, repo: RoleRepository = Depends()):
    """Update a role"""
    role_object = await repo.findOne(credentials.old_role_name)
    update_dict = {}
    update_dict["name"] = credentials.new_role_name
    return await repo.update(role_object.id, update_dict)

@router.delete(path='/')
async def delete_role(credentials: user.RoleInSchema, repo: RoleRepository = Depends()):
    "Delete a role"
    return await repo.remove(credentials.id)