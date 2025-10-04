import enum
from datetime import datetime, UTC

from sqlalchemy import (
    DATE,
    DECIMAL,
    VARCHAR,
    BigInteger,
    Column,
    Enum,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)

from app.core.database import Base


class UserORM(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    username = Column(VARCHAR(36), nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    name = Column(VARCHAR(36), nullable=False)
    phone_number = Column(VARCHAR(15), nullable=False)

    __table_args__ = (
        UniqueConstraint("username", name="uq_username"),
        UniqueConstraint("phone_number", name="uq_phone_number"),
    )


class OrderORM(Base):
    __tablename__ = "orders"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    code = Column(VARCHAR(20), nullable=False)
    price = Column(DECIMAL(19, 4))
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    __table_args__ = (UniqueConstraint("code", name="uq_code_order"),)


class Gender(enum.Enum):
    men = "men"
    women = "women"


class PassengerORM(Base):
    __tablename__ = "passengers"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR(36), nullable=False)
    national_id = Column(VARCHAR(10), nullable=False)
    date_of_birth = Column(DATE, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)


class TicketORM(Base):
    __tablename__ = "tickets"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    ticket_number = Column(VARCHAR(50), nullable=False)
    order_id = Column(BigInteger, ForeignKey("orders.id"), nullable=False)
    passenger_id = Column(BigInteger, ForeignKey("passengers.id"), nullable=False)
    destination_id = Column(BigInteger, ForeignKey("airports.id"), nullable=False)
    origin_id = Column(BigInteger, ForeignKey("airports.id"), nullable=False)
    departure_time = Column(
        DateTime(timezone=True),
        nullable=True,
        default=lambda: datetime.now(UTC),
    )
    arrival_time = Column(
        DateTime(timezone=True),
        nullable=True,
        default=lambda: datetime.now(UTC),
    )

    __table_args__ = (
        UniqueConstraint("ticket_number", name="uq_ticket_number"),
        UniqueConstraint("order_id", "passenger_id", name="uq_order_passenger"),
    )


class AirportORM(Base):
    __tablename__ = "airports"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR(36), nullable=False)
    code = Column(VARCHAR(36), nullable=False)
