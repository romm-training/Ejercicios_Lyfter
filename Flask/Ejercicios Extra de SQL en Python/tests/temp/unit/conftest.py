from datetime import date
from unittest.mock import MagicMock

import pytest

from repositories.car_rental_repository import CarRentalRepository
from repositories.car_repository import CarRepository
from repositories.user_repository import UserRepository
from services.state_machine import Context


@pytest.fixture
def user_row():
    """Fila tal como la devuelve la BD."""
    return (1, "Ana", "ana@mail.com", "ana", date(1990, 1, 1), "active")


@pytest.fixture
def user_dict():
    """Registro ya formateado por UserRepository._format_record."""
    return {
        "id": 1,
        "name": "Ana",
        "email": "ana@mail.com",
        "username": "ana",
        "password": "***",
        "birthdate_at": date(1990, 1, 1),
        "account_status": "active",
    }


@pytest.fixture
def user_payload():
    return {
        "name": "Ana",
        "email": "ana@mail.com",
        "username": "ana",
        "password": "secret",
        "birthdate_at": "1990-01-01",
    }


@pytest.fixture
def db_manager():
    return MagicMock()


@pytest.fixture
def user_repository(db_manager):
    return UserRepository(db_manager)


@pytest.fixture
def car_row():
    return (1, "Toyota", "Corolla", 2020, "available")


@pytest.fixture
def car_dict():
    return {"id": 1, "make": "Toyota", "model": "Corolla", "year": 2020, "status": "available"}


@pytest.fixture
def car_payload():
    return {"make": "Toyota", "model": "Corolla", "year": 2020}


@pytest.fixture
def rental_row():
    return (1, 2, 3, date(2025, 1, 1), date(2025, 1, 5), "pending")


@pytest.fixture
def rental_dict():
    return {
        "id": 1,
        "car_id": 2,
        "user_id": 3,
        "rental_date_at": date(2025, 1, 1),
        "return_date_at": date(2025, 1, 5),
        "status": "pending",
    }


@pytest.fixture
def rental_payload():
    return {"return_date_at": "2025-01-10"}


@pytest.fixture
def car_repository(db_manager):
    return CarRepository(db_manager)


@pytest.fixture
def car_rental_repository(db_manager):
    return CarRentalRepository(db_manager)


@pytest.fixture
def make_ctx():
    def _make(entity="user", current_record=None, data=None, user_repo=None,
              car_repo=None, rental_repo=None):
        return Context(
            entity=entity,
            target_status="active",
            repos={
                "user": user_repo or MagicMock(),
                "car": car_repo or MagicMock(),
                "car_rental": rental_repo or MagicMock(),
            },
            current_record=current_record,
            data=data,
        )
    return _make
