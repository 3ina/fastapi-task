from fastapi import FastAPI
from app.core.config import settings
from contextlib import asynccontextmanager
from app.core.database import Base, engine
from app.interfaces.users_api import router as user_router


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
