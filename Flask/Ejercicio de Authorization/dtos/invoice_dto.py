from dtos.read_base_dto import ReadBaseDTO
from dtos.input_base_dto import InputBaseDTO
from dtos.invoice_detail_dto import InvoiceDetailDTO, InvoiceDetailCreateDTO, InvoiceDetailUpdateDTO
from datetime import date
from decimal import Decimal
from pydantic import Field

class InvoiceDTO(ReadBaseDTO):
    id: int
    user_id: int
    number: str
    created_date: date
    description: str
    total_amount: Decimal
    invoice_details: list[InvoiceDetailDTO]

class InvoiceCreateDTO(InputBaseDTO):
    number: str = Field(max_length=10)
    created_date: date
    description: str = Field(max_length=100)
    invoice_details: list[InvoiceDetailCreateDTO] = Field(min_length=1)

class InvoiceUpdateDTO(InputBaseDTO):
    number: str = Field(max_length=10)
    created_date: date
    description: str = Field(max_length=100)
    invoice_details: list[InvoiceDetailUpdateDTO] = Field(min_length=1)
