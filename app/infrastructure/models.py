import enum
from app.core.database import Base
from sqlalchemy import (
    DATE,
    DECIMAL,
    VARCHAR,
    BigInteger,
    Column,
    Enum,
    ForeignKey,
    UniqueConstraint,
)


class UserORM(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    username = Column(VARCHAR(36), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    name = Column(VARCHAR(36), nullable=False)
    phone_number = Column(VARCHAR(15), nullable=False)

    __table_args__ = (UniqueConstraint("username", name="uq_username"),)


class OrderORM(Base):
    __tablename__ = "orders"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    code = Column(VARCHAR(20), nullable=False)
    price = Column(DECIMAL(19, 4))
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    __table_args__ = (UniqueConstraint("code", name="uq_code_order"),)
