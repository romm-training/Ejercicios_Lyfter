from dtos.read_base_dto import ReadBaseDTO
from dtos.input_base_dto import InputBaseDTO

class UserDTO(ReadBaseDTO):
    id: int
    username: str
    role: str

class UserLoginDTO(InputBaseDTO):
    username: str
    password: str

class UserCreateDTO(InputBaseDTO):
    username: str
    password: str

class UserUpdateDTO(InputBaseDTO):
    password: str
