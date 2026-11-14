from ejercicio3.dtos.read_base_dto import ReadBaseDTO
from ejercicio3.dtos.input_base_dto import InputBaseDTO

class AddressDTO(ReadBaseDTO):
    id: int
    user_id: int
    address: str

class AddressCreateDTO(InputBaseDTO):
    user_id: int
    address: str

class AddressUpdateDTO(InputBaseDTO):
    address: str | None = None


