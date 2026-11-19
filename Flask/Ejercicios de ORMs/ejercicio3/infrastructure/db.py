from sqlalchemy import MetaData, Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)

def create_session_factory(engine: Engine) -> sessionmaker:
    return sessionmaker(engine, expire_on_commit=False)

def create_schema(engine: Engine) -> None:
    import ejercicio3.models
    Base.metadata.create_all(engine)

def drop_schema(engine: Engine) -> None:
    import ejercicio3.models
    Base.metadata.drop_all(engine)
