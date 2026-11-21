from sqlalchemy import Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from roles import Role
from infrastructure.db import Base
from datetime import date
from decimal import Decimal

class Invoice(Base):
    __tablename__ = "invoice"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
        nullable=False
    )

    number: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False
    )

    created_date: Mapped[date] = mapped_column(
        nullable = False
    )

    description: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates = "invoices"
    )

    invoice_details: Mapped[list["InvoiceDetail"]] = relationship(
        back_populates = "invoice"
    )