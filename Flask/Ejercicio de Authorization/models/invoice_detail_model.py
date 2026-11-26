from typing import TYPE_CHECKING
from sqlalchemy import Integer, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from roles import Role
from infrastructure.db import Base
from decimal import Decimal

if TYPE_CHECKING:
    from models.invoice_model import Invoice
    from models.product_model import Product

class InvoiceDetail(Base):
    __tablename__ = "invoice_detail"

    id: Mapped[int] = mapped_column(
        primary_key = True,
        nullable = False
    )

    invoice_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("invoice.id"),
        nullable = False
    )

    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("product.id"),
        nullable = False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable = False
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable = False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=12, scale=2),
        nullable = False
    )

    invoice: Mapped["Invoice"] = relationship(
        back_populates = "invoice_details"
    )
    product: Mapped["Product"] = relationship()