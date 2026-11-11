from sqlalchemy.orm import selectinload

from ejercicio3.repositories.base_repository import BaseRepository

from ejercicio3.models.car_model import Car

class CarRepository(BaseRepository[Car]):
    model = Car
    updatable = frozenset({"plate", "make", "model", "year"})
    load_options = (selectinload(Car.users),)
