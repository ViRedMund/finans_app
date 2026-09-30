from decimal import Decimal

from sqlalchemy import ForeignKey
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)


class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    balance: Mapped[Decimal]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
