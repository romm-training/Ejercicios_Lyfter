from typing import Callable

from ejercicio3.repositories.unit_of_work import UnitOfWork
from ejercicio3.dtos.user_dto import UserDTO, UserCreateDTO, UserUpdateDTO, UserReadDTO

class UserService:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    def create_user(self, data: UserCreateDTO) -> UserDTO:
        with self._uow_factory() as uow:
            user = uow.users.create(
                **data.model_dump()
            )
            uow.commit()
            return UserDTO.model_validate(user)

    def update_user(self, user_id: int, data: UserUpdateDTO) -> UserDTO:
        with self._uow_factory() as uow:
            user = uow.users.update(
                user_id,
                **data.model_dump(
                    exclude_unset=True # Permite modificar parcialmente
                )
            )
            uow.commit()
            return UserDTO.model_validate(user)

    def delete_user(self, user_id: int) -> None:
        with self._uow_factory() as uow:
            uow.users.delete(user_id)
            uow.commit()

    def get_all(self) -> list[UserReadDTO]:
        with self._uow_factory() as uow:
            users = uow.users.get_all()
            return [UserReadDTO.model_validate(user) for user in users]

    def get_by_id(self, user_id: int) -> UserDTO:
        with self._uow_factory() as uow:
            user = uow.users.get_by_id(user_id)
            return UserDTO.model_validate(user)

    def associate_car(self, user_id: int, car_id: int) -> UserReadDTO:
        with self._uow_factory() as uow:
            user = uow.users.associate_car(user_id, car_id)
            uow.commit()
            return UserReadDTO.model_validate(user)

    def disassociate_car(self, user_id: int, car_id: int):
        with self._uow_factory() as uow:
            uow.users.disassociate_user_car(user_id, car_id)
            uow.commit()
