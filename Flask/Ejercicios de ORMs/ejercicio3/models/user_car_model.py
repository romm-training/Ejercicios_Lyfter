from sqlalchemy import Column, ForeignKey, Table

from ejercicio3.infrastructure.db import Base

user_car = Table(
    "user_car",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("car_id", ForeignKey("car.id"), primary_key=True)
)