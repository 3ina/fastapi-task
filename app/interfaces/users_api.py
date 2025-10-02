from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.util.langhelpers import repr_tuple_names
from app.services import userService
from app.services.userService import UserService
from app.core.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


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
    try:
        return await user_service.register_user(
            username=data.username,
            password=data.password,
            name=data.name,
            phone_number=data.phone_number,
        )
    except Exception as e:
        pass
