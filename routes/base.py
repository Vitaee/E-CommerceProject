from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from .auth import router as auth
from .products import router as product
from .business import router as business
from .category import router as category
from tasks.users import send_confirmation_email

router = APIRouter()
router.include_router(auth, prefix='/auth', tags=['Authentication'])
router.include_router(product, prefix='/products', tags=['Products'])
router.include_router(category, prefix='/category', tags=['Category'])
router.include_router(business, prefix='/business', tags=['Business'])


@router.get('/', include_in_schema=False, )
async def home(request: Request) -> JSONResponse:
    return JSONResponse(status_code=200, content={"message": "Base route"})
