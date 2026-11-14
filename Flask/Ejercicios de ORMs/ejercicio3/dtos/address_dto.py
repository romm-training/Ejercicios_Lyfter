from pydantic import EmailStr

from ejercicio3.dtos.read_base_dto import ReadBaseDTO
from ejercicio3.dtos.input_base_dto import InputBaseDTO

class AddressDTO(ReadBaseDTO):
    id: int
    user_id: int
    email_address: EmailStr

class AddressCreateDTO(InputBaseDTO):
    user_id: int
    email_address: EmailStr

class AddressUpdateDTO(InputBaseDTO):
    email_address: EmailStr | None = None


