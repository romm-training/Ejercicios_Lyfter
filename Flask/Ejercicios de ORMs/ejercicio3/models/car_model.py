from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ejercicio3.infrastructure.db import Base

if TYPE_CHECKING:
    from ejercicio3.models.user_model import User

class Car(Base):
    __tablename__ = "car"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"), nullable=True)
    plate: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    make: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)

    user: Mapped["User | None"] = relationship(
        back_populates="cars"
    )

