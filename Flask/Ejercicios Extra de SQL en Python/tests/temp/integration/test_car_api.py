import pytest

from api_paths import CARS, NON_EXISTENT_ID


def _put(client, car, **overrides):
    body = {"make": car["make"], "model": car["model"], "year": car["year"], **overrides}
    return client.put(f"{CARS}/{car['id']}", json=body)


class TestCreate:
    def test_creates_available_car(self, make_car, car_data):
        data = car_data()
        car = make_car(**data)

        assert car["status"] == "available"
        assert (car["make"], car["model"], car["year"]) == (data["make"], data["model"], data["year"])

    def test_ignores_status_sent_by_client(self, make_car):
        assert make_car(status="sold")["status"] == "available"

    def test_missing_field_returns_500(self, client, car_data):
        data = car_data()
        del data["year"]

        assert client.post(f"{CARS}/", json=data).status_code == 500


class TestRead:
    def test_get_by_id(self, client, make_car):
        car = make_car()

        resp = client.get(f"{CARS}/{car['id']}")

        assert resp.status_code == 200
        assert resp.get_json() == car

    def test_get_by_id_not_found(self, client):
        assert client.get(f"{CARS}/{NON_EXISTENT_ID}").status_code == 404

    def test_get_all_filtered_by_make(self, client, make_car):
        car = make_car()
        make_car()

        resp = client.get(f"{CARS}/?make={car['make']}")

        assert resp.status_code == 200
        assert [c["id"] for c in resp.get_json()] == [car["id"]]

    def test_get_all_without_matches_returns_empty_list(self, client):
        resp = client.get(f"{CARS}/?make=no_existe_zzz")

        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_get_all_invalid_filter_returns_422(self, client):
        assert client.get(f"{CARS}/?color=red").status_code == 422


class TestUpdate:
    def test_updates_fields(self, client, make_car):
        car = make_car()

        resp = _put(client, car, model="Yaris", year=2022)

        assert resp.status_code == 200
        body = client.get(f"{CARS}/{car['id']}").get_json()
        assert (body["model"], body["year"], body["status"]) == ("Yaris", 2022, "available")

    def test_not_found(self, client, car_data):
        assert client.put(f"{CARS}/{NON_EXISTENT_ID}", json=car_data()).status_code == 404

    def test_missing_field_returns_500(self, client, make_car):
        car = make_car()
        assert client.put(f"{CARS}/{car['id']}", json={"make": "x"}).status_code == 500

    def test_available_to_maintenance_and_back(self, client, make_car):
        car = make_car()

        assert _put(client, car, status="maintenance").get_json()["status"] == "maintenance"
        assert _put(client, car, status="available").get_json()["status"] == "available"

    def test_available_to_inactive_then_sold(self, client, make_car):
        car = make_car()

        assert _put(client, car, status="inactive").get_json()["status"] == "inactive"
        assert _put(client, car, status="sold").get_json()["status"] == "sold"

    @pytest.mark.parametrize("target", ["rented", "reserved"])
    def test_available_cannot_jump_to_rental_states(self, client, make_car, target):
        car = make_car()

        assert _put(client, car, status=target).status_code == 409
        assert client.get(f"{CARS}/{car['id']}").get_json()["status"] == "available"

    @pytest.mark.parametrize("final", ["sold"])
    def test_final_state_cannot_change(self, client, make_car, final):
        car = make_car()
        _put(client, car, status=final)

        assert _put(client, car, status="available").status_code == 409

    def test_unknown_status_returns_409(self, client, make_car):
        assert _put(client, make_car(), status="inventado").status_code == 409

    def test_reserved_car_cannot_go_to_maintenance(self, client, make_user, make_car, make_rental):
        user, car = make_user(), make_car()
        make_rental(user, car)

        assert _put(client, car, status="maintenance").status_code == 409
        assert client.get(f"{CARS}/{car['id']}").get_json()["status"] == "reserved"


class TestDelete:
    def test_deletes_car(self, client, make_car):
        car = make_car()

        assert client.delete(f"{CARS}/{car['id']}").status_code == 204
        assert client.get(f"{CARS}/{car['id']}").status_code == 404

    def test_delete_car_with_rentals_fails_and_keeps_car(self, client, make_user, make_car, make_rental):
        user, car = make_user(), make_car()
        make_rental(user, car)

        assert client.delete(f"{CARS}/{car['id']}").status_code == 500
        assert client.get(f"{CARS}/{car['id']}").status_code == 200

    def test_delete_non_existent_car_is_idempotent(self, client):
        assert client.delete(f"{CARS}/{NON_EXISTENT_ID}").status_code == 204
