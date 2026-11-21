from datetime import datetime, timezone
from typing import Callable

from dtos.auth_dto import TokenDTO, RefreshTokenDTO
from dtos.user_dto import UserLoginDTO
from exceptions import NotFoundError, InvalidCredentialsError, InvalidTokenError
from repositories.unit_of_work import UnitOfWork
from services.protocols import PasswordHasher, TokenSigner, TokenVerifier

class AuthenticationService():    
    def __init__(
        self, 
        uow_factory: Callable[[],UnitOfWork],
        hasher: PasswordHasher,
        access_signer: TokenSigner,
        refresh_signer: TokenSigner,
        refresh_verifier: TokenVerifier
    ) -> None:
        self._uow_factory = uow_factory
        self._hasher = hasher
        self._access_signer = access_signer
        self._refresh_signer = refresh_signer
        self._refresh_verifier = refresh_verifier

    def login(self, data: UserLoginDTO) -> TokenDTO:
        with self._uow_factory() as uow:
            try:
                user = uow.users.get_by_username(data.username)
            except NotFoundError:
                raise InvalidCredentialsError()
            
            if not self._hasher.verify(data.password, user.password):
                raise InvalidCredentialsError()

            tokens = self._issue_tokens(uow, user.id, user.role)
            uow.commit(

            )
            return tokens

    def refresh(self, data: RefreshTokenDTO) -> TokenDTO:
        payload = self._refresh_verifier.decode(data.refresh_token)

        with self._uow_factory() as uow:
            try:
                stored = uow.refresh_tokens.get_by_jti(payload["jti"])
            except (NotFoundError):
                raise InvalidTokenError()

            if stored.revoked:
                # Reutilizacion: se asume robo y se invalidan todas las sesiones.
                uow.refresh_tokens.revoke_all_by_user_id(stored.user_id)
                uow.commit() # antes de lanzar: __exit__ hace rollback ante excepciones
                raise InvalidTokenError()

            try:
                user = uow.users.get_by_id(stored.user_id)
            except NotFoundError:
                raise InvalidTokenError()

            uow.refresh_tokens.update(stored.id, revoked=True)
            tokens = self._issue_tokens(uow, user.id, user.role)
            uow.commit()
            return tokens

    def logout(self, data: RefreshTokenDTO) -> None:
        payload = self._refresh_verifier.decode(data.refresh_token)

        with self._uow_factory() as uow:
            try:
                stored = uow.refresh_tokens.get_by_jti(payload["jti"])
            except NotFoundError:
                return 
            uow.refresh_tokens.update(stored.id, revoked=True)
            uow.commit()
                

    def _issue_tokens(self, uow: UnitOfWork, user_id: int, role: str) -> TokenDTO:
        access_token = self._access_signer.encode(
            {"sub": str(user_id), "role": role}
        ),
        refresh_token = self._refresh_signer.encode(
            {"sub": str(user_id)}
        )
        claims = self._refresh_verifier.decode(refresh_token)
        uow.refresh_tokens_create(
            jti=claims["jti"],
            user_id=user_id,
            expires_at=datetime.fromtimestamp(claims["exp"],tz=timezone.utc)
        )
        return TokenDTO(
            access_token=access_token,
            refresh_token=refresh_token
            )
