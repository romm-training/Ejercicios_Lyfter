from sqlalchemy import create_engine, Table, Column, Integer, String
from sqlalchemy import MetaData, ForeignKey

DB_URI = "postgresql://postgres:ClaveSimple123@localhost:5432/EjerciciosDeOrm"
engine = create_engine(DB_URI, echo=True)

metadata_obj = MetaData()

user_table = Table(
    "user",    
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("full_name", String)
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user.id"), nullable=False),
    Column("address", String, nullable=False)
)

car_table = Table(
    "car",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id"), nullable=True),
    Column("plate", String, unique=True, nullable=False),
    Column("make", String, nullable=False),
    Column("model", String, nullable=False),
    Column("year", Integer, nullable=False)
)

#metadata_obj.drop_all(engine)
metadata_obj.create_all(engine)