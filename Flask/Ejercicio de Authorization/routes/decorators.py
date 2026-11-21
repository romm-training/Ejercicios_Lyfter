from functools import wraps

from flask import g, request

from exceptions import AuthorizationError, InvalidTokenError
from services.protocols import TokenVerifier

class AuthenticationGuard:
    def __init__(self, verifier: TokenVerifier) -> None:
        self._verifier = verifier

    def require_authentication(self, view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            self._authenticate()
            return view(*args, **kwargs)
        return wrapper

    def require_role(self, *roles: str):
        def decorator(view):
            @wraps(view)
            def wrapper(*args, **kwargs):
                payload = self._authenticate()
                if payload.get("role") not in roles:
                    raise AuthorizationError()
                return view(*args, **kwargs)
            return wrapper
        return decorator

    def _authenticate(self) -> dict:
        header = request.headers.get("Authorization", "")
        scheme, _, token = header.partition(" ")
        if scheme.lower() != "bearer" or not token:
            raise InvalidTokenError()
        payload = self._verifier.decode(token)
        g.current_user = payload
        return payload