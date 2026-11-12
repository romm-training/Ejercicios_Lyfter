from typing import Any, ClassVar, Generic, Sequence, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ejercicio3.exceptions import InvalidFieldError, NotFoundError, ConflictError

from ejercicio3.infrastructure.db import Base

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    model: ClassVar[type[T]]
    updatable: ClassVar[frozenset[str]] = frozenset()
    load_options: ClassVar[tuple] = ()

    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> Sequence[T]:
        stmt = select(self.model).options(*self.load_options)
        return self._session.scalars(stmt).all()

    def get_by_id(self, entity_id: int) -> T:
        entity = self._session.get(
            self.model, 
            entity_id,
            options=self.load_options
        )
        if entity is None:
            raise NotFoundError(f"{self.model.__name__} con id {entity_id} no encontrado.")
        return entity

    def create(self, **data: Any) -> T:
        entity = self.model(**data)
        self._session.add(entity)
        try:
            self._session.flush()
        except IntegrityError as e:
            raise ConflictError(f"{self.model.__name__} duplicado.") from e
        return entity

    def update(self, entity_id: int, **data: Any) -> T:
        invalid = data.keys() - self.updatable
        if invalid:
            raise InvalidFieldError(f"Campos no modificables: {sorted(invalid)}")
        entity = self.get_by_id(entity_id)
        for field, value in data.items():
            setattr(entity, field, value)
        try:
            self._session.flush()
        except IntegrityError as e:
            raise ConflictError(f"{self.model.__name__} no pudo ser actualizado.")
        return entity

    def delete(self, entity_id: int) -> None:
        self._session.delete(self.get_by_id(entity_id))
        self._session.flush()
