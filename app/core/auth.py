from app.core.config import settings
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

SECERT_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRES_SECONDS = 1200
REFRESH_TOKEN_EXPIRES_SECONDS = 900


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_text: str, hashed_password: str) -> bool:
    try:
        value = pwd_context.verify(plain_text, hashed_password)
    except ValueError:
        return False
    return value


def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRES_SECONDS):
    """
    set expires_delta in second
    """

    to_encode = data.copy()
    to_encode.update(
        {
            "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_delta),
            "type": "access",
        }
    )
