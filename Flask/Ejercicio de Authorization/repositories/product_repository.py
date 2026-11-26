from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session

from repositories.base_repository import BaseRepository

from models.product_model import Product

from exceptions import NotFoundError

class ProductRepository(BaseRepository[Product]):
    model = Product
    updatable = frozenset({"name", "price", "received_date", "stock"})

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_id_for_update(self, product_id: int) -> Product:
        stmt = select(Product).where(
            Product.id == product_id
            ).with_for_update()
        product = self._session.scalars(stmt).one_or_none()
        if product is None:
            raise NotFoundError(f"Producto con id {id} no encontrado.")
        return product