from typing import Callable
from decimal import Decimal

from repositories.unit_of_work import UnitOfWork
from repositories.product_repository import ProductRepository
from dtos.invoice_dto import InvoiceDTO, InvoiceCreateDTO, InvoiceUpdateDTO
from models.invoice_detail_model import InvoiceDetail
from exceptions import NotFoundError

class InvoiceService:
    def __init__(
            self,
            uow_factory: Callable[[], UnitOfWork]
            ) -> None:
        self._uow_factory = uow_factory
    
    def create(
            self, 
            user_id:int, 
            data: InvoiceCreateDTO
            ) -> InvoiceDTO:
        with self._uow_factory() as uow:
            details = []
            for detail in data.invoice_details:
                product = uow.products.get_by_id(detail.product_id)
                price = Decimal(str(product.price))
                amount = price * detail.quantity

                invoice_detail = InvoiceDetail(
                    product_id = detail.product_id,
                    quantity = detail.quantity,
                    price = price,
                    amount = amount
                )

                details.append(invoice_detail)

            total_amount = sum(d.amount for d in details)

            invoice = uow.invoices.create(
                user_id = user_id,
                number = data.number,
                created_date = data.created_date,
                description = data.description,
                total_amount = total_amount,
                invoice_details = details
            )

            uow.commit()
            return InvoiceDTO.model_validate(invoice)

    def get_all_by_user_id(
            self, 
            user_id: int
            ) -> list[InvoiceDTO]:
        with self._uow_factory() as uow:
            invoices = uow.invoices.get_by_user_id(user_id)
            return [
                InvoiceDTO.model_validate(invoice) for invoice in invoices
                ]

    def get_by_id(
            self,
            invoice_id: int,
            user_id: int | None = None
            ) -> InvoiceDTO:
        with self._uow_factory() as uow:
            invoice = uow.invoices.get_by_id(invoice_id)
            if user_id is not None and invoice.user_id != user_id:
                raise NotFoundError()
            return InvoiceDTO.model_validate(invoice)

    def get_all(self) -> list[InvoiceDTO]:
        with self._uow_factory() as uow:
            invoices = uow.invoices.get_all()
            return [
                InvoiceDTO.model_validate(invoice) for invoice in invoices
                ]
            

