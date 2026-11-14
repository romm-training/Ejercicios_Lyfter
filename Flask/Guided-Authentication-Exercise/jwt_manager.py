import jwt
from datetime import datetime, timedelta, timezone

class JWTManager():
    def __init__(self, secret, algorithm, access_expiration, refresh_expiration):
        self.secret = secret
        self.algorithm = algorithm
        self.access_expiration = access_expiration
        self.refresh_expiration = refresh_expiration

    def encode(self, data, expires_in):
        payload = {
            **data,
            "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        }
        try:
            return jwt.encode(payload, self.secret, algorithm=self.algorithm)
        except (jwt.PyJWTError, TypeError) as error:
            print(f"Error generando el token: {error}")
            return None
        
    def decode(self, token):
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.PyJWTError as error:
            print(f"Token invalido: {error}")
            return None

    def generate_tokens(self, user_id):
        access_token = self.encode({"id": user_id, "type": "access"}, self.access_expiration)
        refresh_token = self.encode({"id": user_id, "type": "refresh"}, self.refresh_expiration)
        return access_token, refresh_token

    def decode_token(self, token, expected_type):
        decoded = self.decode(token)
        # Un token valido pero de otro tipo se rechaza igual que uno invalido
        if decoded is None or decoded.get("type") != expected_type:
            return None
        return decoded

