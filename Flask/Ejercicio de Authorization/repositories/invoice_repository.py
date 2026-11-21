from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session

from repositories.base_repository import BaseRepository
from exceptions import NotFoundError

from models.invoice_model import Invoice

class InvoiceRepository(BaseRepository[Invoice]):
    model = Invoice
    updatable = frozenset({
        "number",
        "created_date",
        "description"
        })
    load_options = (selectinload(Invoice.invoice_details),)

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_user_id(self, user_id:int) -> list[Invoice]:
        stmt = (
            select(self.model)
            .where(self.model.user_id==user_id)
            .options(*self.load_options)
        )
        entities = self._session.scalars(stmt).all()
        return entities