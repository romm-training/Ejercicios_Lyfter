"""Fixtures de integración: Flask real + PostgreSQL real (variables del .env).

Las pruebas crean sus propios datos con valores únicos y los borran al terminar;
no tocan los datos de ejemplo. Si no hay conexión a la BD, se omiten.
"""
import os
import uuid
from pathlib import Path

import pytest
from dotenv import load_dotenv
from flask import Flask

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")
if not os.environ.get("STATUS_TRANSITIONS_PATH"):
    os.environ["STATUS_TRANSITIONS_PATH"] = "config/state_transitions.yaml"

from infrastructure.db import PgManager  # noqa: E402
from repositories.car_rental_repository import CarRentalRepository  # noqa: E402
from repositories.car_repository import CarRepository  # noqa: E402
from repositories.user_repository import UserRepository  # noqa: E402
from routes.car_rental_routes import register_car_rental_routes  # noqa: E402
from routes.car_routes import register_car_routes  # noqa: E402
from routes.user_routes import register_user_routes  # noqa: E402
from routes.error_handlers import register_error_handlers
from services.car_rental_service import CarRentalService  # noqa: E402
from services.car_service import CarService  # noqa: E402
from services.state_machine import build_state_machine  # noqa: E402
from services.user_service import UserService  # noqa: E402

from api_paths import CARS, RENTALS, USERS  # noqa: E402


def pytest_collection_modifyitems(items):
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)


@pytest.fixture(scope="session")
def db():
    try:
        manager = PgManager.from_env()
    except KeyError as e:
        pytest.skip(f"Falta la variable de entorno {e}.")
    if not getattr(manager, "cursor", None):
        pytest.skip("No hay conexión a PostgreSQL.")
    yield manager
    manager.close_connection()


@pytest.fixture(scope="session")
def client(db):
    app = Flask(__name__)
    state_machine = build_state_machine(db)
    register_error_handlers(app)
    register_user_routes(app, UserService(UserRepository(db), state_machine, db))
    register_car_routes(app, CarService(CarRepository(db), state_machine, db))
    register_car_rental_routes(app, CarRentalService(CarRentalRepository(db), state_machine, db))
    return app.test_client()


@pytest.fixture
def created_ids():
    return {"users": [], "cars": []}


@pytest.fixture(autouse=True)
def cleanup(db, created_ids):
    """Borra lo creado por la prueba (alquileres primero por las FK)."""
    yield
    users, cars = created_ids["users"], created_ids["cars"]
    if not users and not cars:
        return
    db.execute_query(
        "DELETE FROM lyfter_car_rental.car_rental WHERE car_id = ANY(%s) OR user_id = ANY(%s);",
        (cars, users),
    )
    db.execute_query("DELETE FROM lyfter_car_rental.car WHERE id = ANY(%s);", (cars,))
    db.execute_query('DELETE FROM lyfter_car_rental."user" WHERE id = ANY(%s);', (users,))


def _uid():
    return uuid.uuid4().hex[:8]


@pytest.fixture
def user_data():
    def _build(**overrides):
        uid = _uid()
        data = {
            "name": "Test User",
            "email": f"it_{uid}@mail.com",
            "username": f"it_{uid}",
            "password": "secret",
            "birthdate_at": "1990-01-01",
        }
        return {**data, **overrides}
    return _build


@pytest.fixture
def car_data():
    def _build(**overrides):
        data = {"make": f"Mk{_uid()}", "model": "Corolla", "year": 2020}
        return {**data, **overrides}
    return _build


@pytest.fixture
def make_user(client, created_ids, user_data):
    def _make(**overrides):
        resp = client.post(f"{USERS}/", json=user_data(**overrides))
        assert resp.status_code == 201, resp.get_json()
        user = resp.get_json()
        created_ids["users"].append(user["id"])
        return user
    return _make


@pytest.fixture
def make_car(client, created_ids, car_data):
    def _make(**overrides):
        resp = client.post(f"{CARS}/", json=car_data(**overrides))
        assert resp.status_code == 201, resp.get_json()
        car = resp.get_json()
        created_ids["cars"].append(car["id"])
        return car
    return _make


@pytest.fixture
def rental_data():
    def _build(user, car, **overrides):
        data = {
            "user_id": user["id"],
            "car_id": car["id"],
            "return_date_at": "2025-01-05 10:00:00",
        }
        return {**data, **overrides}
    return _build


@pytest.fixture
def make_rental(client, rental_data):
    def _make(user, car, **overrides):
        resp = client.post(f"{RENTALS}/", json=rental_data(user, car, **overrides))
        assert resp.status_code == 201, resp.get_json()
        return resp.get_json()
    return _make


@pytest.fixture
def set_status(db):
    """Fuerza un estado directo en la BD (para preparar escenarios)."""
    tables = {
        "user": ('lyfter_car_rental."user"', "account_status"),
        "car": ("lyfter_car_rental.car", "status"),
        "car_rental": ("lyfter_car_rental.car_rental", "status"),
    }

    def _set(entity, record_id, status):
        table, column = tables[entity]
        db.execute_query(f"UPDATE {table} SET {column} = %s WHERE id = %s;", (status, record_id))
    return _set


@pytest.fixture
def rental_put():
    """Cuerpo válido del PUT de alquileres (la ruta exige las tres llaves vacías)."""
    def _body(**overrides):
        body = {
            "return_date_at": "2025-01-10 10:00:00",
        }
        return {**body, **overrides}
    return _body
