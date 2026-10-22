import pytest

from api_paths import CARS, NON_EXISTENT_ID, RENTALS, USERS


def _car_status(client, car):
    return client.get(f"{CARS}/{car['id']}").get_json()["status"]


def _user_status(client, user):
    return client.get(f"{USERS}/{user['id']}").get_json()["account_status"]


def _rental_status(client, rental):
    return client.get(f"{RENTALS}/{rental['id']}").get_json()["status"]


@pytest.fixture
def move(client, rental_put):
    """PUT de alquiler que solicita un cambio de estado."""
    def _move(rental, status):
        return client.put(f"{RENTALS}/{rental['id']}", json=rental_put(status=status))
    return _move


@pytest.fixture
def setup(make_user, make_car, make_rental):
    user, car = make_user(), make_car()
    return user, car, make_rental(user, car)


class TestCreate:
    def test_creates_pending_rental_and_reserves_car(self, client, make_user, make_car, make_rental):
        user, car = make_user(), make_car()

        rental = make_rental(user, car, status="completed")

        assert rental["status"] == "pending"
        assert (rental["user_id"], rental["car_id"]) == (user["id"], car["id"])
        assert _car_status(client, car) == "reserved"

    def test_car_not_available_returns_422(self, client, make_user, make_car, make_rental, rental_data):
        user, car = make_user(), make_car()
        make_rental(user, car)

        resp = client.post(f"{RENTALS}/", json=rental_data(make_user(), car))

        assert resp.status_code == 422
        assert _car_status(client, car) == "reserved"

    def test_inactive_user_returns_422_and_leaves_car_untouched(
        self, client, make_user, make_car, rental_data, set_status
    ):
        user, car = make_user(), make_car()
        set_status("user", user["id"], "inactive")

        resp = client.post(f"{RENTALS}/", json=rental_data(user, car))

        assert resp.status_code == 422
        assert _car_status(client, car) == "available"

    def test_delinquent_user_returns_422(self, client, make_user, make_car, rental_data, set_status):
        user, car = make_user(), make_car()
        set_status("user", user["id"], "delinquent")

        assert client.post(f"{RENTALS}/", json=rental_data(user, car)).status_code == 422

    def test_non_existent_car_returns_404(self, client, make_user, rental_data):
        user = make_user()

        resp = client.post(f"{RENTALS}/", json=rental_data(user, {"id": NON_EXISTENT_ID}))

        assert resp.status_code == 404

    def test_non_existent_user_returns_404_and_car_stays_available(
        self, client, make_car, rental_data
    ):
        car = make_car()

        resp = client.post(f"{RENTALS}/", json=rental_data({"id": NON_EXISTENT_ID}, car))

        assert resp.status_code == 404
        assert _car_status(client, car) == "available"

    def test_missing_field_returns_500(self, client, make_user, make_car, rental_data):
        user, car = make_user(), make_car()
        data = rental_data(user, car)
        del data["return_date_at"]

        assert client.post(f"{RENTALS}/", json=data).status_code == 500
        assert _car_status(client, car) == "available"

    def test_rental_date_at_not_allowed_returns_422(self, client, make_user, make_car, rental_data):
        user, car = make_user(), make_car()

        resp = client.post(f"{RENTALS}/", json=rental_data(user, car, rental_date_at="2025-01-01"))

        assert resp.status_code == 422
        assert _car_status(client, car) == "available"


class TestRead:
    def test_get_by_id(self, client, setup):
        _, _, rental = setup

        resp = client.get(f"{RENTALS}/{rental['id']}")

        assert resp.status_code == 200
        assert resp.get_json()["id"] == rental["id"]

    def test_get_by_id_not_found(self, client):
        assert client.get(f"{RENTALS}/{NON_EXISTENT_ID}").status_code == 404

    def test_get_all_filtered_by_user(self, client, setup):
        user, _, rental = setup

        resp = client.get(f"{RENTALS}/?user_id={user['id']}&status=pending")

        assert resp.status_code == 200
        assert [r["id"] for r in resp.get_json()] == [rental["id"]]

    def test_get_all_without_matches_returns_empty_list(self, client):
        resp = client.get(f"{RENTALS}/?user_id={NON_EXISTENT_ID}")

        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_get_all_invalid_filter_returns_422(self, client):
        assert client.get(f"{RENTALS}/?color=red").status_code == 422


class TestUpdate:
    def test_updates_return_date_only(self, client, setup, rental_put):
        _, _, rental = setup

        resp = client.put(f"{RENTALS}/{rental['id']}", json=rental_put(return_date_at="2025-02-01 08:00:00"))

        assert resp.status_code == 200
        body = client.get(f"{RENTALS}/{rental['id']}").get_json()
        assert "2025" in body["return_date_at"] and "01 Feb" in body["return_date_at"]
        assert body["status"] == "pending"

    @pytest.mark.parametrize("field, value", [("car_id", 1), ("user_id", 1), ("rental_date_at", "2025-01-01")])
    def test_forbidden_fields_return_422(self, client, setup, rental_put, field, value):
        _, _, rental = setup

        resp = client.put(f"{RENTALS}/{rental['id']}", json=rental_put(**{field: value}))

        assert resp.status_code == 422

    def test_not_found(self, client, rental_put):
        assert client.put(f"{RENTALS}/{NON_EXISTENT_ID}", json=rental_put()).status_code == 404

    def test_missing_forbidden_keys_is_accepted(self, client, setup):
        _, _, rental = setup

        resp = client.put(f"{RENTALS}/{rental['id']}", json={"return_date_at": "2025-02-01"})

        assert resp.status_code == 200


class TestStatusFlow:
    def test_pending_to_active_rents_car(self, client, setup, move):
        _, car, rental = setup

        resp = move(rental, "active")

        assert resp.status_code == 200
        assert resp.get_json()["status"] == "active"
        assert _car_status(client, car) == "rented"

    def test_active_to_completed_releases_car(self, client, setup, move):
        _, car, rental = setup
        move(rental, "active")

        resp = move(rental, "completed")

        assert resp.status_code == 200
        assert resp.get_json()["status"] == "completed"
        assert _car_status(client, car) == "available"

    def test_pending_to_cancelled_releases_car(self, client, setup, move):
        _, car, rental = setup

        resp = move(rental, "cancelled")

        assert resp.status_code == 200
        assert resp.get_json()["status"] == "cancelled"
        assert _car_status(client, car) == "available"

    def test_car_can_be_rented_again_after_completion(self, client, setup, move, make_user, make_rental):
        _, car, rental = setup
        move(rental, "active")
        move(rental, "completed")

        new_rental = make_rental(make_user(), car)

        assert new_rental["status"] == "pending"
        assert _car_status(client, car) == "reserved"

    @pytest.mark.parametrize("path, target", [
        ([], "completed"),
        ([], "overdue"),
        (["active"], "pending"),
        (["active"], "cancelled"),
        (["cancelled"], "active"),
        (["active", "completed"], "active"),
        (["active", "completed"], "cancelled"),
    ])
    def test_invalid_transitions_return_409(self, client, setup, move, path, target):
        _, _, rental = setup
        for step in path:
            assert move(rental, step).status_code == 200
        before = _rental_status(client, rental)

        resp = move(rental, target)

        assert resp.status_code == 409
        assert _rental_status(client, rental) == before

    def test_unknown_status_returns_409(self, setup, move):
        _, _, rental = setup
        assert move(rental, "inventado").status_code == 409

    def test_activation_fails_if_user_became_inactive_and_rolls_back(self, client, setup, move, set_status):
        user, car, rental = setup
        set_status("user", user["id"], "inactive")

        resp = move(rental, "active")

        assert resp.status_code == 422
        assert _rental_status(client, rental) == "pending"
        assert _car_status(client, car) == "reserved"

    def test_activation_fails_if_car_not_reserved(self, client, setup, move, set_status):
        _, car, rental = setup
        set_status("car", car["id"], "maintenance")

        resp = move(rental, "active")

        assert resp.status_code == 422
        assert _rental_status(client, rental) == "pending"

    def test_completion_fails_if_car_not_rented(self, client, setup, move, set_status):
        _, car, rental = setup
        move(rental, "active")
        set_status("car", car["id"], "maintenance")

        resp = move(rental, "completed")

        assert resp.status_code == 422
        assert _rental_status(client, rental) == "active"

    def test_failed_transition_does_not_update_return_date(self, client, setup, rental_put):
        _, _, rental = setup
        body = rental_put(status="completed", return_date_at="2030-01-01 00:00:00")

        assert client.put(f"{RENTALS}/{rental['id']}", json=body).status_code == 409
        assert "2030" not in client.get(f"{RENTALS}/{rental['id']}").get_json()["return_date_at"]

    @pytest.mark.xfail(reason="user_to_delinquent usa ctx.current_record[id] en vez del id (KeyError en user_rules.py).")
    def test_active_to_overdue_marks_user_delinquent(self, client, setup, move):
        user, car, rental = setup
        move(rental, "active")

        resp = move(rental, "overdue")

        assert resp.status_code == 200
        assert _rental_status(client, rental) == "overdue"
        assert _user_status(client, user) == "delinquent"
        assert _car_status(client, car) == "rented"

    @pytest.mark.xfail(reason="user_to_active usa ctx.current_record[id] en vez del id (KeyError en user_rules.py).")
    def test_overdue_to_completed_reactivates_user_and_releases_car(self, client, setup, move, set_status):
        user, car, rental = setup
        move(rental, "active")
        set_status("car_rental", rental["id"], "overdue")
        set_status("user", user["id"], "delinquent")

        resp = move(rental, "completed")

        assert resp.status_code == 200
        assert _rental_status(client, rental) == "completed"
        assert _user_status(client, user) == "active"
        assert _car_status(client, car) == "available"


class TestDelete:
    def test_deletes_rental(self, client, setup):
        _, _, rental = setup

        assert client.delete(f"{RENTALS}/{rental['id']}").status_code == 204
        assert client.get(f"{RENTALS}/{rental['id']}").status_code == 404

    def test_delete_non_existent_rental_is_idempotent(self, client):
        assert client.delete(f"{RENTALS}/{NON_EXISTENT_ID}").status_code == 204
