from ejercicio3.repositories.base_repository import BaseRepository

from ejercicio3.models.address_model import Address


class AddressRepository(BaseRepository[Address]):
    model = Address
    updatable = frozenset({"email_address"})
