from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ejercicio3.infrastructure.db import Base
from ejercicio3.models.user_car_model import user_car

if TYPE_CHECKING:
    from ejercicio3.models.address_model import Address
    from ejercicio3.models.car_model import Car

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    full_name: Mapped[str] = mapped_column(String(100))

    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )

    cars: Mapped[list["Car"]] = relationship(
        secondary=user_car, 
        back_populates="users"
    )

