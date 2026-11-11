from ejercicio3.dtos.read_base_dto import ReadBaseDTO
from ejercicio3.dtos.input_base_dto import InputBaseDTO

class CarDTO(ReadBaseDTO):
    id: int
    plate: str
    make: str
    model: str
    year: int

class CarCreateDTO(InputBaseDTO):
    id: int
    plate: str
    make: str
    model: str
    year: int

class CarUpdateDTO(InputBaseDTO):
    plate: str | None = None
    make: str | None = None
    model: str | None = None
    year: int | None = None

