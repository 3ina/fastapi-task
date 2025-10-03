from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_text: str, hashed_password: str) -> bool:
    try:
        value = pwd_context.verify(plain_text, hashed_password)
    except ValueError:
        return False
    return value
