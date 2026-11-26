from typing import Callable

from repositories.unit_of_work import UnitOfWork
from dtos.user_dto import UserDTO, UserCreateDTO, UserUpdateDTO
from services.protocols import PasswordHasher

class UserService:
    def __init__(
            self, 
            uow_factory: Callable[[], UnitOfWork], 
            hasher: PasswordHasher
            ) -> None:
        self._uow_factory = uow_factory
        self._hasher = hasher

    def create(self, data: UserCreateDTO) -> UserDTO:
        with self._uow_factory() as uow:
            user = uow.users.create(
                username=data.username,
                password=self._hasher.hash(data.password)
            )
            uow.commit()
            return UserDTO.model_validate(user)

    def update(self, user_id: int, data: UserUpdateDTO) -> UserDTO:
        with self._uow_factory() as uow:
            user = uow.users.update(
                user_id,
                password=self._hasher.hash(data.password)
            )
            uow.commit()
            return UserDTO.model_validate(user)

    def delete(self, user_id: int) -> None:
        with self._uow_factory() as uow:
            uow.users.delete(
                user_id
            )
            uow.commit()

    def get_all(self) -> list[UserDTO]:
        with self._uow_factory() as uow:
            users = uow.users.get_all()
            return [UserDTO.model_validate(user) for user in users]

    def get_by_id(self, user_id: int) -> UserDTO:
        with self._uow_factory() as uow:
            user = uow.users.get_by_id(user_id)
            return UserDTO.model_validate(user)
