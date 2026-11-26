from dtos.read_base_dto import ReadBaseDTO
from dtos.input_base_dto import InputBaseDTO
from decimal import Decimal
from pydantic import Field

class InvoiceDetailDTO(ReadBaseDTO):
    id: int
    invoice_id: int
    product_id: int
    quantity: int
    price: Decimal
    amount: Decimal

class InvoiceDetailCreateDTO(InputBaseDTO):
    product_id: int
    quantity: int = Field(gt=0)

class InvoiceDetailUpdateDTO(InputBaseDTO):
    product_id: int
    quantity: int = Field(gt=0)

