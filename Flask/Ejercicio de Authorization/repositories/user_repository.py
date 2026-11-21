from sqlalchemy import select
from sqlalchemy.orm import selectinload, Session

from repositories.base_repository import BaseRepository
from exceptions import NotFoundError

from models.user_model import User

class UserRepository(BaseRepository[User]):
    model = User
    updatable = frozenset({"password"})

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_username(self, username:str) -> User:
        stmt = (
            select(self.model)
            .where(self.model.username==username)
        )
        entity = self._session.scalars(stmt).first()
        if entity is None:
            raise NotFoundError()
        return entity
