from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from exceptions import InvalidTokenError

_ALGORITHM = "RS256"

class JwtSigner:
    def __init__(
            self,
            private_key: str,
            issuer: str,
            audience: str,
            expires_minutes: int = 15
    ) -> None:
        self._private_key = private_key
        self._issuer = issuer
        self._audience = audience
        self._expires = timedelta(minutes=expires_minutes)

    def encode(self, payload: dict[str, Any]) -> str:
        now = datetime.now(timezone.utc)
        claims = {
            **payload,
            "iss": self._issuer,
            "aud": self._audience,
            "iat": now,
            "exp": now + self._expires
        }
        return jwt.encode(
            claims, 
            self._private_key, 
            algorithm=_ALGORITHM
            )

class JwtVerifier:
    def __init__(self, public_key: str, issuer: str, audience: str) -> None:
        self._public_key = public_key
        self._issuer = issuer
        self._audience = audience

    def decode(self, token: str) -> dict[str, Any]:
        try:
            return jwt.decode(
                token,
                self._public_key,
                algorithms=[_ALGORITHM],
                issuer=self._issuer,
                audience=self._audience,
                options={
                    "require": ["exp","iat","iss","aud","sub"]
                }
            )
        except jwt.InvalidTokenError as exc:
            raise InvalidTokenError() from exc