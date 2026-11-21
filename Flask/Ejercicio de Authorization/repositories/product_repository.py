from sqlalchemy.orm import selectinload, Session

from repositories.base_repository import BaseRepository

from models.product_model import Product

class ProductRepository(BaseRepository[Product]):
    model = Product
    updatable = frozenset({"name", "price", "received_date", "stock"})

    def __init__(self, session: Session) -> None:
        super().__init__(session)
        