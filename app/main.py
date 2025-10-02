from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.core.config import settings
from contextlib import asynccontextmanager
from app.core.database import Base, engine
from app.interfaces.users_api import router as user_router
from app.exceptions.baseExcption import AppException


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Top company task API",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.include_router(user_router)


@app.exception_handler(AppException)
async def generic_app_error_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=500,
        content={"detail": f"{str(exc)}"},
    )
