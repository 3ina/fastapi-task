# app/services/exceptions.py
from app.exceptions.baseExcption import ServiceException


class UserAlreadyExistsException(ServiceException):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        super().__init__(f"User with {field} '{value}' already exists.")


class IncorrectCredentialsException(ServiceException):
    pass


class IncorrectPasswordException(ServiceException):
    pass
