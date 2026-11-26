from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from roles import Role
from infrastructure.db import Base

if TYPE_CHECKING:
    from models.invoice_model import Invoice

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True
        )
    username: Mapped[str] = mapped_column(
        String(30), 
        unique=True,
        nullable=False
        )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
        )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=Role.USER.value
    )

    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="user"
    )