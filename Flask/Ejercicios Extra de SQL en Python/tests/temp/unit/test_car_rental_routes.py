from unittest.mock import MagicMock

import pytest
from flask import Flask

from exceptions import BusinessRuleError, InvalidTransitionError, NotFoundError
from routes.car_rental_routes import register_car_rental_routes
from routes.error_handlers import register_error_handlers

BASE = "/api/v1/rentals"


@pytest.fixture
def service():
    return MagicMock()


@pytest.fixture
def client(service):
    app = Flask(__name__)
    register_error_handlers(app)
    register_car_rental_routes(app, service)
    return app.test_client()


@pytest.fixture
def create_payload():
    return {
        "user_id": 3,
        "car_id": 2,
        "return_date_at": "2025-01-05",
        "status": "pending",
    }


ERROR_CASES = [
    (BusinessRuleError("regla"), 422),
    (InvalidTransitionError("x"), 409),
    (RuntimeError("boom"), 500),
]


class TestGetAll:
    def test_ok_passes_query_args_as_filters(self, client, service):
        service.get_all_rentals.return_value = [{"id": 1}]

        resp = client.get(f"{BASE}/?status=pending")

        assert resp.status_code == 200
        assert resp.get_json() == [{"id": 1}]
        service.get_all_rentals.assert_called_once_with({"status": "pending"})

    def test_no_results_returns_empty_list(self, client, service):
        service.get_all_rentals.return_value = []

        resp = client.get(f"{BASE}/")

        assert resp.status_code == 200
        assert resp.get_json() == []

    @pytest.mark.parametrize("error, status", ERROR_CASES)
    def test_errors(self, client, service, error, status):
        service.get_all_rentals.side_effect = error
        assert client.get(f"{BASE}/").status_code == status

    def test_business_rule_message_is_exposed(self, client, service):
        service.get_all_rentals.side_effect = BusinessRuleError("filtro malo")
        assert "filtro malo" in client.get(f"{BASE}/").get_json()["error"]


class TestGetById:
    def test_ok(self, client, service):
        service.get_rental_by_id.return_value = {"id": 1}

        resp = client.get(f"{BASE}/1")

        assert resp.status_code == 200
        assert resp.get_json() == {"id": 1}
        service.get_rental_by_id.assert_called_once_with(1)

    def test_non_integer_id_is_404(self, client):
        assert client.get(f"{BASE}/abc").status_code == 404

    @pytest.mark.parametrize("error, status", ERROR_CASES + [(NotFoundError("x"), 404)])
    def test_errors(self, client, service, error, status):
        service.get_rental_by_id.side_effect = error
        assert client.get(f"{BASE}/1").status_code == status


class TestCreate:
    def test_created(self, client, service, create_payload):
        service.create_rental.return_value = {"id": 1}

        resp = client.post(f"{BASE}/", json=create_payload)

        assert resp.status_code == 201
        assert resp.get_json() == {"id": 1}
        service.create_rental.assert_called_once_with(create_payload)

    def test_rental_date_at_not_allowed_returns_422(self, client, service, create_payload):
        resp = client.post(f"{BASE}/", json={**create_payload, "rental_date_at": "2025-01-01"})

        assert resp.status_code == 422
        service.create_rental.assert_not_called()

    @pytest.mark.parametrize("error, status", ERROR_CASES + [(NotFoundError("x"), 404)])
    def test_errors(self, client, service, create_payload, error, status):
        service.create_rental.side_effect = error
        assert client.post(f"{BASE}/", json=create_payload).status_code == status


class TestUpdate:
    def test_ok(self, client, service, rental_payload):
        service.update_rental.return_value = {"id": 1}
        body = {**rental_payload}

        resp = client.put(f"{BASE}/1", json=body)

        assert resp.status_code == 200
        assert resp.get_json() == {"id": 1}
        service.update_rental.assert_called_once_with(1, body)

    @pytest.mark.parametrize("field, value", [
        ("car_id", 2), ("user_id", 3), ("rental_date_at", "2025-01-01"),
    ])
    def test_forbidden_fields_return_422(self, client, service, rental_payload, field, value):
        body = {**rental_payload, field: value}

        resp = client.put(f"{BASE}/1", json=body)

        assert resp.status_code == 422
        service.update_rental.assert_not_called()

    @pytest.mark.parametrize("error, status", ERROR_CASES + [(NotFoundError("x"), 404)])
    def test_errors(self, client, service, rental_payload, error, status):
        service.update_rental.side_effect = error
        assert client.put(f"{BASE}/1", json=rental_payload).status_code == status


class TestDelete:
    def test_no_content(self, client, service):
        resp = client.delete(f"{BASE}/1")

        assert resp.status_code == 204
        assert resp.data == b""
        service.delete_rental.assert_called_once_with(1)

    @pytest.mark.parametrize("error, status", ERROR_CASES + [(NotFoundError("x"), 404)])
    def test_errors(self, client, service, error, status):
        service.delete_rental.side_effect = error
        assert client.delete(f"{BASE}/1").status_code == status
