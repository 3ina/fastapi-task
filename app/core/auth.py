from datetime import datetime, timedelta, UTC

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.core.dependencies import get_user_service
from app.infrastructure.models import UserORM
from app.services.userService import UserService

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRES_SECONDS = 1200
REFRESH_TOKEN_EXPIRES_SECONDS = 900


oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token/swagger")


def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRES_SECONDS):
    """
    set expires_delta in second
    """

    to_encode = data.copy()
    to_encode.update(
        {
            "exp": datetime.now(UTC) + timedelta(seconds=expires_delta),
            "type": "access",
        }
    )

    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def create_refresh_token(
    data: dict, expires_delta: int = REFRESH_TOKEN_EXPIRES_SECONDS
) -> str:
    """
    set expires_delta in second
    """

    to_encode = data.copy()
    to_encode.update(
        {
            "exp": datetime.now(UTC) + timedelta(seconds=expires_delta),
            "type": "refresh",
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_schema),
    user_service: UserService = Depends(get_user_service),
) -> UserORM:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise credentials_exception
        username: str | None = payload.get("sub")

        if username is None:
            raise credentials_exception

        user = await user_service.get_by_username(username=username)

        return user
    except JWTError as e:
        if "exp" in str(e):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
        raise credentials_exception from e
