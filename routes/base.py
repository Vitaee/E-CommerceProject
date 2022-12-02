from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse
from .auth import router as auth
from tasks.users import send_confirmation_email

router = APIRouter()
router.include_router(auth, prefix='/auth', tags=['Authentication'])


@router.get('/', include_in_schema=False, )
async def home(request: Request) -> JSONResponse:
    return JSONResponse(status_code=200, content={"message": "Base route"})
