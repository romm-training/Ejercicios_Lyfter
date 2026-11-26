from typing import Callable

from repositories.unit_of_work import UnitOfWork
from dtos.product_dto import ProductDTO, ProductCreateDTO, ProductUpdateDTO

class ProductService:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    def create(self, data: ProductCreateDTO) -> ProductDTO:
        with self._uow_factory() as uow:
            product = uow.products.create(
                **data.model_dump() 
            )
            uow.commit()
            return ProductDTO.model_validate(product)

    def update(self, product_id: int, data: ProductUpdateDTO) -> ProductDTO:
        with self._uow_factory() as uow:
            product = uow.products.update(
                product_id,
                **data.model_dump(
                    exclude_unset=True # Modificacion parcial
                )
            )
            uow.commit()
            return ProductDTO.model_validate(product)

    def delete(self, product_id: int) -> None:
        with self._uow_factory() as uow:
            uow.products.delete(product_id)
            uow.commit()

    def get_all(self) -> list[ProductDTO]:
        with self._uow_factory() as uow:
            products = uow.products.get_all()
            return [ProductDTO.model_validate(product) for product in products]

    def get_by_id(self, product_id: int) -> ProductDTO:
        with self._uow_factory() as uow:
            product = uow.products.get_by_id(product_id)
            return ProductDTO.model_validate(product)