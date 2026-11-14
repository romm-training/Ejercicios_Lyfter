from typing import Callable

from ejercicio3.repositories.unit_of_work import UnitOfWork
from ejercicio3.dtos.car_dto import CarDTO, CarCreateDTO, CarUpdateDTO

class CarService:
    def __init__(self, uow_factory: Callable[[],UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    def create_car(self, data: CarCreateDTO) -> CarDTO:
        with self._uow_factory() as uow:
            car = uow.cars.create(
                **data.model_dump()
            )
            uow.commit()
            return CarDTO.model_validate(car)

    def update_car(self, car_id: int, data: CarUpdateDTO) -> CarDTO:
        with self._uow_factory() as uow:
            car = uow.cars.update(
                car_id,
                **data.model_dump(
                    exclude_unset=True #Permite modificar parcialmente
                )
            )
            uow.commit()
            return CarDTO.model_validate(car)

    def delete_car(self, car_id: int) -> None:
        with self._uow_factory() as uow:
            uow.cars.delete(car_id)
            uow.commit()

    def get_all(self) -> list[CarDTO]:
        with self._uow_factory() as uow:
            cars = uow.cars.get_all()
            return [CarDTO.model_validate(car) for car in cars]

    def get_by_id(self, car_id: int) -> CarDTO:
        with self._uow_factory() as uow:
            car = uow.cars.get_by_id(car_id)
            return CarDTO.model_validate(car)
