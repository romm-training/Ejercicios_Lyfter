import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from exceptions import InvalidTokenError
from token_type import TokenType

_ALGORITHM = "RS256"

class JwtSigner:
    def __init__(
            self,
            private_key: str,
            issuer: str,
            audience: str,
            token_type: TokenType,
            expires_delta: timedelta
    ) -> None:
        self._private_key = private_key
        self._issuer = issuer
        self._audience = audience
        self._token_type = token_type
        self._expires = expires_delta

    def encode(self, payload: dict[str, Any]) -> str:
        now = datetime.now(timezone.utc)
        claims = {
            **payload,
            "type": self._token_type.value,
            "jti": str(uuid.uuid4()),
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
    def __init__(
            self, 
            public_key: str, 
            issuer: str, 
            audience: str,
            expected_type: TokenType
    ) -> None:
        self._public_key = public_key
        self._issuer = issuer
        self._audience = audience
        self._expected_type = expected_type

    def decode(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                self._public_key,
                algorithms=[_ALGORITHM],
                issuer=self._issuer,
                audience=self._audience,
                options={
                    "require": ["exp","iat","iss","aud","sub","type","jti"]
                }
            )
        except jwt.InvalidTokenError as exc:
            raise InvalidTokenError() from exc

        if payload["type"] != self._expected_type.value:
            raise InvalidTokenError()
        return payload