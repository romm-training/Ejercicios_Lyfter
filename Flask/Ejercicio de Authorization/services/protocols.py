from typing import Any, Protocol

class PasswordHasher(Protocol):
    def hash(self, plain: str) -> str: ...

    def verify(self, plain: str, hashed: str) -> bool: ...

class TokenSigner(Protocol):
    def encode(self, payload: dict[str, Any]) -> str: ...

class TokenVerifier(Protocol):
    def decode(self, token: str) -> dict[str, Any]: ...
        

