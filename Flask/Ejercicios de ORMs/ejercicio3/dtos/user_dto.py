from ejercicio3.dtos.read_base_dto import ReadBaseDTO
from ejercicio3.dtos.input_base_dto import InputBaseDTO

from ejercicio3.dtos.car_dto import CarDTO
from ejercicio3.dtos.address_dto import AddressDTO

class UserDTO(ReadBaseDTO):
    id: int
    name: str
    full_name: str

class UserCreateDTO(InputBaseDTO):
    id: int
    name: str
    full_name: str

class UserUpdateDTO(InputBaseDTO):
    name: str | None = None
    full_name: str | None = None

class UserReadDTO(UserDTO):
    cars: list[CarDTO] = []
    addresses: list[AddressDTO] = []

