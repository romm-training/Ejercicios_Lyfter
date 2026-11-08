from unittest.mock import MagicMock

import pytest
from flask import Flask

from exceptions import BusinessRuleError, InvalidTransitionError, NotFoundError
from routes.user_routes import register_user_routes
from routes.error_handlers import register_error_handlers

BASE = "/api/v1/users"


@pytest.fixture
def service():
    return MagicMock()


@pytest.fixture
def client(service):
    app = Flask(__name__)
    register_error_handlers(app)
    register_user_routes(app, service)
    return app.test_client()


ERROR_CASES = [
    (BusinessRuleError("regla"), 422),
    (InvalidTransitionError("x"), 409),
    (RuntimeError("boom"), 500),
]


class TestGetAll:
    def test_ok_passes_query_args_as_filters(self, client, service):
        service.get_all_users.return_value = [{"id": 1}]

        resp = client.get(f"{BASE}/?username=ana")

        assert resp.status_code == 200
        assert resp.get_json() == [{"id": 1}]
        service.get_all_users.assert_called_once_with({"username": "ana"})

    def test_no_results_returns_empty_list(self, client, service):
        service.get_all_users.return_value = []

        resp = client.get(f"{BASE}/")

        assert resp.status_code == 200
        assert resp.get_json() == []

    @pytest.mark.parametrize("error, status", ERROR_CASES)
    def test_errors(self, client, service, error, status):
        service.get_all_users.side_effect = error
        assert client.get(f"{BASE}/").status_code == status

    def test_business_rule_message_is_exposed(self, client, service):
        service.get_all_users.side_effect = BusinessRuleError("filtro malo")
        assert "filtro malo" in client.get(f"{BASE}/").get_json()["error"]


class TestGetById:
    def test_ok(self, client, service):
        service.get_user_by_id.return_value = {"id": 1}

        resp = client.get(f"{BASE}/1")

        assert resp.status_code == 200
        assert resp.get_json() == {"id": 1}
        service.get_user_by_id.assert_called_once_with(1)

    def test_non_integer_id_is_404(self, client):
        assert client.get(f"{BASE}/abc").status_code == 404

    @pytest.mark.parametrize("error, status", ERROR_CASES + [(NotFoundError("x"), 404)])
    def test_errors(self, client, service, error, status):
        service.get_user_by_id.side_effect = error
        assert client.get(f"{BASE}/1").status_code == status


class TestCreate:
    def test_created(self, client, service, user_payload):
        service.create_user.return_value = {"id": 1}

        resp = client.post(f"{BASE}/", json=user_payload)

        assert resp.status_code == 201
        assert resp.get_json() == {"id": 1}
        service.create_user.assert_called_once_with(user_payload)

    @pytest.mark.parametrize("error, status", ERROR_CASES + [(NotFoundError("x"), 404)])
    def test_errors(self, client, service, user_payload, error, status):
        service.create_user.side_effect = error
        assert client.post(f"{BASE}/", json=user_payload).status_code == status


class TestUpdate:
    def test_ok(self, client, service, user_payload):
        service.update_user.return_value = {"id": 1}

        resp = client.put(f"{BASE}/1", json=user_payload)

        assert resp.status_code == 200
        assert resp.get_json() == {"id": 1}
        service.update_user.assert_called_once_with(1, user_payload)

    @pytest.mark.parametrize("error, status", ERROR_CASES + [(NotFoundError("x"), 404)])
    def test_errors(self, client, service, user_payload, error, status):
        service.update_user.side_effect = error
        assert client.put(f"{BASE}/1", json=user_payload).status_code == status


class TestDelete:
    def test_no_content(self, client, service):
        resp = client.delete(f"{BASE}/1")

        assert resp.status_code == 204
        assert resp.data == b""
        service.delete_user.assert_called_once_with(1)

    @pytest.mark.parametrize("error, status", ERROR_CASES + [(NotFoundError("x"), 404)])
    def test_errors(self, client, service, error, status):
        service.delete_user.side_effect = error
        assert client.delete(f"{BASE}/1").status_code == status
