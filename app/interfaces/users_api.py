from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import BaseModel

from app.core.auth import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    create_refresh_token,
)
from app.core.dependencies import get_user_service, get_user_selector
from app.services.userService import UserService
from app.selectors.userSelector import UserSelector

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/token/swagger", include_in_schema=False)
async def login_for_swagger(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_access_token({"sub": user.username})
    refresh = create_refresh_token({"sub": user.username})

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
    }


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/token")
async def login_endpoint(
    form_data: LoginRequest,
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access = create_access_token({"sub": user.username})
    refresh = create_refresh_token({"sub": user.username})
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
    }


class RefreshToken(BaseModel):
    refresh_token: str


@router.post("/refresh")
async def refresh_token(
    refresh_token_input: RefreshToken,
    user_selector: UserSelector = Depends(get_user_selector),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = jwt.decode(
        refresh_token_input.refresh_token, SECRET_KEY, algorithms=[ALGORITHM]
    )
    if payload.get("type") != "refresh":
        raise credentials_exception
    username: str | None = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = await user_selector.get_by_username(username=username)
    if not user:
        raise credentials_exception

    new_access_token = create_access_token(
        {
            "sub": user.username,
        }
    )

    return {"access_token": new_access_token, "token_type": "bearer"}


class CreateUserRequest(BaseModel):
    username: str
    password: str
    name: str
    phone_number: str


class UserData(BaseModel):
    id: int
    username: str


class CreateUserResponse(BaseModel):
    message: str
    data: UserData


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CreateUserResponse,
)
async def create_user(
    data: CreateUserRequest, user_service: UserService = Depends(get_user_service)
):
    return await user_service.register_user(
        username=data.username,
        password=data.password,
        name=data.name,
        phone_number=data.phone_number,
    )
