from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.db import Base

class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(
        primary_key=True
        )
    name: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    price: Mapped[float] = mapped_column(
        nullable=False
    )
    received_date: Mapped[date] = mapped_column(
        nullable=False
    )
    stock: Mapped[int] = mapped_column(
        nullable=False
    )