from sqlalchemy.orm import Session, sessionmaker

from ejercicio3.repositories.address_repository import AddressRepository
from ejercicio3.repositories.car_repository import CarRepository
from ejercicio3.repositories.user_repository import UserRepository

class UnitOfWork:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory
        self._session = None


    def __enter__(self) -> "UnitOfWork":
        self._session = self._session_factory()
        self.addresses = AddressRepository(self._session)
        self.cars = CarRepository(self._session)
        self.users = UserRepository(self._session)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            if exc_type is not None:
                self._session.rollback()
        finally:
            self._session.close()

    def commit(self) -> None:
        self._session.commit()