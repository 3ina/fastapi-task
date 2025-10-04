from passlib.context import CryptContext
from datetime import date
import random
import string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_text: str, hashed_password: str) -> bool:
    try:
        value = pwd_context.verify(plain_text, hashed_password)
    except ValueError:
        return False
    return value


def calculate_age(birth_date):
    today = date.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    return age


def generate_random_code(length=6):
    characters = string.ascii_uppercase + string.digits
    return "".join(random.choices(characters, k=length))
