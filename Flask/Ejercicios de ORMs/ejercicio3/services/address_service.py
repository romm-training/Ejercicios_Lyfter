from typing import Callable

from ejercicio3.repositories.unit_of_work import UnitOfWork
from ejercicio3.dtos.address_dto import AddressDTO, AddressCreateDTO, AddressUpdateDTO

class AddressService:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    def create_address(self, data: AddressCreateDTO) -> AddressDTO:
        with self._uow_factory() as uow:
            uow.users.get_by_id(data.user_id)
            
            address = uow.addresses.create(
                **data.model_dump() # convierte el DTO en **kwargs para el repository, así que el service no nombra ningún campo.
            )
            uow.commit()
            return AddressDTO.model_validate(address)

    def update_address(self, address_id: int, data: AddressUpdateDTO) -> AddressDTO:
        with self._uow_factory() as uow:
            
            address = uow.addresses.update(
                address_id, 
                **data.model_dump(
                    exclude_unset=True # permite modificar parcialmente. Solo viaja lo que el llamador envió.
                )
            )
            uow.commit()
            return AddressDTO.model_validate(address)

    def delete_address(self, address_id: int) -> None:
        with self._uow_factory() as uow:
            uow.addresses.delete(address_id)
            uow.commit()

    def get_all(self) -> list[AddressDTO]:
        with self._uow_factory() as uow:
            addresses = uow.addresses.get_all()
            return [AddressDTO.model_validate(address) for address in addresses]

    def get_by_id(self, address_id: int) -> AddressDTO:
        with self._uow_factory() as uow:
            address = uow.addresses.get_by_id(address_id)
            return AddressDTO.model_validate(address)
