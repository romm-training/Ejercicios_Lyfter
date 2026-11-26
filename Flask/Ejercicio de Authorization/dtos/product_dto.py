from dtos.read_base_dto import ReadBaseDTO
from dtos.input_base_dto import InputBaseDTO
from datetime import date

class ProductDTO(ReadBaseDTO):
    id: int
    name: str
    price: float
    received_date: date
    stock: int

class ProductCreateDTO(InputBaseDTO):
    name: str
    price: float
    received_date: date
    stock: int

class ProductUpdateDTO(InputBaseDTO):
    name: str
    price: float
    received_date: date
    stock: int
