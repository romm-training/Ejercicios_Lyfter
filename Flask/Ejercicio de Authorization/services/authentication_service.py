from typing import Callable

from dtos.auth_dto import TokenDTO
from dtos.user_dto import UserLoginDTO
from exceptions import NotFoundError, InvalidCredentialsError
from repositories.unit_of_work import UnitOfWork
from services.protocols import PasswordHasher, TokenSigner


class AuthenticationService():    
    def __init__(
        self, 
        uow_factory: Callable[[],UnitOfWork],
        hasher: PasswordHasher,
        token_signer: TokenSigner
    ) -> None:
        self._uow_factory = uow_factory
        self._hasher = hasher
        self._token_signer = token_signer

    def login(self, data: UserLoginDTO) -> TokenDTO:
        with self._uow_factory() as uow:
            try:
                user = uow.users.get_by_username(data.username)
            except NotFoundError:
                raise InvalidCredentialsError()
            
            if not self._hasher.verify(data.password, user.password):
                raise InvalidCredentialsError()

            payload = {"sub": str(user.id), "role": user.role }

            return TokenDTO(access_token=self._token_signer.encode(payload))