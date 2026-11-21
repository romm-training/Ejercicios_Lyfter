from sqlalchemy.orm import Session, sessionmaker

from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository
from repositories.invoice_repository import InvoiceRepository

class UnitOfWork:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory
        self._session = None

    def __enter__(self) -> "UnitOfWork":
        self._session = self._session_factory()
        self.products = ProductRepository(self._session)
        self.users = UserRepository(self._session)
        self.invoices = InvoiceRepository(self._session)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            if exc_type is not None:
                self._session.rollback()
        finally:
            self._session.close()

    def commit(self) -> None:
        self._session.commit()