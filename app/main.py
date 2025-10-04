from contextlib import asynccontextmanager


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import Base, engine
from app.exceptions.baseExcption import AppException
from app.interfaces.users_api import router as user_router
from app.interfaces.passengers_api import router as passenger_router
from app.interfaces.airports_api import router as airport_router
from app.interfaces.flights_api import router as flight_router


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
app.include_router(passenger_router)
app.include_router(airport_router)
app.include_router(flight_router)


@app.exception_handler(AppException)
async def generic_app_error_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=500,
        content={"detail": f"{str(exc)}"},
    )


# TODO : imeplememt exceptions handler for user not found
