from sqlalchemy import select, update
from sqlalchemy.orm import Session

from exceptions import NotFoundError
from models.refresh_token_model import RefreshToken
from repositories.base_repository import BaseRepository

class RefreshTokenRepository(BaseRepository[RefreshToken]):
    model = RefreshToken
    updatable = frozenset({"revoked"})

    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_jti(self, jti: str) -> RefreshToken:
        stmt = select(self.model).where(self.model.jti == jti)
        entity = self._session.scalars(stmt).first()
        if entity is None:
            raise NotFoundError()
        return entity

    def renove_all_by_user_id(self, user_id: int) -> None:
        stmt = (
            update(self.model)
            .where(self.model.user_id == user_id)
            .values(revoked=True)
        )
        self._session.execute(stmt)
