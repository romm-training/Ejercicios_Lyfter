import logging, os, sys 
from flask import Flask
from dotenv import load_dotenv
from functools import partial
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from datetime import timedelta

from exceptions import ConfigurationError
from token_type import TokenType

from infrastructure.db import Base, create_schema, create_session_factory
from infrastructure.jwt_provider import JwtSigner, JwtVerifier
from infrastructure.password_hasher import WerkzeugPasswordHasher

from dtos.product_dto import ProductDTO, ProductCreateDTO, ProductUpdateDTO
from dtos.user_dto import UserDTO, UserCreateDTO, UserUpdateDTO
from dtos.invoice_dto import InvoiceDTO, InvoiceCreateDTO, InvoiceUpdateDTO

from repositories.unit_of_work import UnitOfWork

from services.product_service import ProductService
from services.user_service import UserService
from services.authentication_service import AuthenticationService
from services.protocols import PasswordHasher, TokenSigner, TokenVerifier
from services.invoice_service import InvoiceService

from routes.product_routes import register_product_routes
from routes.user_routes import register_user_routes
from routes.authentication_routes import register_authentication_routes
from routes.decorators import AuthenticationGuard
from routes.error_handlers import register_error_handlers
from routes.invoice_routes import register_invoice_routes

logger = logging.getLogger(__name__)

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",    
    )

def get_database_url() -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL no esta configurada en las variables de entorno")
    return url

BASE_DIR = Path(__file__).resolve().parent
JWT_ISSUER = "authorization-exercise"
JWT_AUDIENCE = "authorization-exercise-api"

def read_key(env_name: str) -> str:
    path = os.getenv(env_name)
    if not path:
        raise ConfigurationError(f"{env_name} no esta configurada")
    return (BASE_DIR / path).read_text()

def get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if not value:
        return default
    
    try:
        parsed = int(value)
    except ValueError:
        raise ConfigurationError(f"{name} debe ser un entero, recibido: {value!r}")
    
    if parsed <= 0:
        raise ConfigurationError(f"{name} debe ser mayor que cero")
    
    return parsed

def build_product_service(
        session_factory: sessionmaker) -> ProductService:
    return ProductService(partial(UnitOfWork, session_factory))

def build_invoice_service(
        session_factory: sessionmaker) -> InvoiceService:
    return InvoiceService(partial(UnitOfWork, session_factory))

def build_user_service(
            session_factory: sessionmaker,
            hasher: PasswordHasher
        ) -> UserService:
    return UserService(
            partial(UnitOfWork, session_factory), 
            hasher
        )

def build_authentication_service(
        session_factory: sessionmaker,
        hasher: PasswordHasher,
        access_signer: TokenSigner,
        refresh_signer: TokenSigner,
        refresh_verifier: TokenVerifier
        ) -> AuthenticationService:
    return AuthenticationService(
        partial(UnitOfWork, session_factory),
        hasher,
        access_signer,
        refresh_signer,
        refresh_verifier
    )


app = Flask(__name__)

register_error_handlers(app)

if __name__ == "__main__":
    load_dotenv()
    configure_logging()
    engine = None

    try:
        engine = create_engine(get_database_url(), pool_pre_ping=True)
        create_schema(engine)
        session_factory = create_session_factory(engine)

        hasher = WerkzeugPasswordHasher()

        private_key = read_key("JWT_PRIVATE_KEY_PATH")
        public_key = read_key("JWT_PUBLIC_KEY_PATH")

        access_signer = JwtSigner(
            private_key, JWT_ISSUER, JWT_AUDIENCE,
            TokenType.ACCESS,
            timedelta(minutes=get_int_env("ACCESS_TOKEN_EXPIRES_MINUTES",15))
        )

        refresh_signer = JwtSigner(
            private_key, JWT_ISSUER, JWT_AUDIENCE,
            TokenType.REFRESH,
            timedelta(days=get_int_env("REFRESH_TOKEN_EXPIRES_DAYS",7))
        )

        access_verifier = JwtVerifier(
            public_key, JWT_ISSUER, JWT_AUDIENCE, TokenType.ACCESS
        )

        refresh_verifier = JwtVerifier(
            public_key, JWT_ISSUER, JWT_AUDIENCE, TokenType.REFRESH
        )

        guard = AuthenticationGuard(access_verifier)

        product_service = build_product_service(session_factory)
        invoice_service = build_invoice_service(session_factory)
        user_service = build_user_service(session_factory, hasher)
        authentication_service = build_authentication_service(
            session_factory,
            hasher,
            access_signer,
            refresh_signer,
            refresh_verifier
        )

        register_product_routes(app, product_service, guard)
        register_invoice_routes(app, invoice_service, guard)
        register_user_routes(app, user_service, guard)
        register_authentication_routes(app, authentication_service, guard)

    except ValidationError as ve:
        logger.error(f"Datos invalidos: {ve}")
    
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True, use_reloader=False)