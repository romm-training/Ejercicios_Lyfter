from werkzeug.security import check_password_hash, generate_password_hash

class WerkzeugPasswordHasher:
    def hash(self, plain: str) -> str:
        return generate_password_hash(plain)

    def verify(self, plain: str, hashed: str) -> bool:
        return check_password_hash(hashed, plain)
    