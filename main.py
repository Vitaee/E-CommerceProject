from fastapi import FastAPI, Request, status
from loguru import logger
from core.exceptions import (
    BadCredentialsError,
    TokenInvalidError,
    TokenExpirateError,
    UnAuthorizedError
)
from routes.base import router
from database.base import connect_db, Tortoise
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from core.utils import format_validation_errors
from core.middlewares import register_cors
from core.logger import register_logs
from core.utils import register_signals

app = FastAPI()

logger = register_logs(app)

@app.on_event('startup')
async def on_start():
    logger.info('App is starting up..')
    register_cors(app)
    register_signals()
    await connect_db(app)

@app.on_event('shutdown')
async def on_shotdown():
    logger.info('Shutting down the application..')
    await Tortoise.close_connections()


app.include_router(router)


@app.middleware("http")
async def error_handling(request: Request, call_next):
    try:
        return await call_next(request)
    except (BadCredentialsError, ) as exc:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={'reason': str(exc)})
    except (TokenExpirateError, TokenInvalidError) as exc:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content={'reason': str(exc)})
    except UnAuthorizedError as exc:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={'reason': str(exc)},
                            headers={"WWW-Authenticate": "Bearer"})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "errors":  format_validation_errors(exc.errors())
            }
    )