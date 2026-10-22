import pytest

from api_paths import CARS, NON_EXISTENT_ID, RENTALS, USERS


class TestCreate:
    def test_creates_active_user(self, client, make_user, user_data):
        data = user_data()
        user = make_user(**data)

        assert user["account_status"] == "active"
        assert user["username"] == data["username"]
        assert data["password"] not in str(user)

    def test_ignores_status_sent_by_client(self, make_user):
        assert make_user(account_status="delinquent")["account_status"] == "active"

    def test_duplicate_username_returns_422(self, client, make_user, user_data):
        user = make_user()

        resp = client.post(f"{USERS}/", json=user_data(username=user["username"]))

        assert resp.status_code == 422

    def test_duplicate_email_returns_422(self, client, make_user, user_data):
        user = make_user()

        resp = client.post(f"{USERS}/", json=user_data(email=user["email"]))

        assert resp.status_code == 422

    def test_missing_field_returns_500(self, client, user_data):
        data = user_data()
        del data["email"]

        assert client.post(f"{USERS}/", json=data).status_code == 500


class TestRead:
    def test_get_by_id(self, client, make_user):
        user = make_user()

        resp = client.get(f"{USERS}/{user['id']}")

        assert resp.status_code == 200
        assert resp.get_json()["username"] == user["username"]

    def test_get_by_id_not_found(self, client):
        assert client.get(f"{USERS}/{NON_EXISTENT_ID}").status_code == 404

    def test_get_all_filtered_by_username(self, client, make_user):
        user = make_user()
        make_user()

        resp = client.get(f"{USERS}/?username={user['username']}")

        assert resp.status_code == 200
        assert [u["id"] for u in resp.get_json()] == [user["id"]]

    def test_get_all_without_matches_returns_empty_list(self, client):
        resp = client.get(f"{USERS}/?username=no_existe_zzz")

        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_get_all_invalid_filter_returns_422(self, client):
        assert client.get(f"{USERS}/?password=x").status_code == 422


class TestUpdate:
    def test_updates_fields(self, client, make_user, user_data):
        user = make_user()
        body = user_data(username=user["username"], email=user["email"], name="Nuevo Nombre")

        resp = client.put(f"{USERS}/{user['id']}", json=body)

        assert resp.status_code == 200
        assert resp.get_json()["name"] == "Nuevo Nombre"
        assert client.get(f"{USERS}/{user['id']}").get_json()["name"] == "Nuevo Nombre"

    def test_not_found(self, client, user_data):
        assert client.put(f"{USERS}/{NON_EXISTENT_ID}", json=user_data()).status_code == 404

    def test_active_to_inactive_and_back(self, client, make_user, user_data):
        user = make_user()
        base = user_data(username=user["username"], email=user["email"])

        resp = client.put(f"{USERS}/{user['id']}", json={**base, "account_status": "inactive"})
        assert resp.status_code == 200
        assert resp.get_json()["account_status"] == "inactive"

        resp = client.put(f"{USERS}/{user['id']}", json={**base, "account_status": "active"})
        assert resp.status_code == 200
        assert resp.get_json()["account_status"] == "active"

    def test_invalid_transition_returns_409_and_keeps_status(self, client, make_user, user_data, set_status):
        user = make_user()
        set_status("user", user["id"], "inactive")
        base = user_data(username=user["username"], email=user["email"])

        resp = client.put(f"{USERS}/{user['id']}", json={**base, "account_status": "delinquent"})

        assert resp.status_code == 409
        assert client.get(f"{USERS}/{user['id']}").get_json()["account_status"] == "inactive"

    def test_unknown_status_returns_409(self, client, make_user, user_data):
        user = make_user()
        base = user_data(username=user["username"], email=user["email"])

        resp = client.put(f"{USERS}/{user['id']}", json={**base, "account_status": "inventado"})

        assert resp.status_code == 409

    def test_cannot_deactivate_user_with_open_rental(self, client, make_user, make_car, make_rental, user_data):
        user, car = make_user(), make_car()
        make_rental(user, car)
        base = user_data(username=user["username"], email=user["email"])

        resp = client.put(f"{USERS}/{user['id']}", json={**base, "account_status": "inactive"})

        assert resp.status_code == 422
        assert client.get(f"{USERS}/{user['id']}").get_json()["account_status"] == "active"

    def test_delinquent_to_active_without_overdue_rentals(self, client, make_user, user_data, set_status):
        user = make_user()
        set_status("user", user["id"], "delinquent")
        base = user_data(username=user["username"], email=user["email"])

        resp = client.put(f"{USERS}/{user['id']}", json={**base, "account_status": "active"})

        assert resp.status_code == 200
        assert resp.get_json()["account_status"] == "active"

    def test_delinquent_to_active_blocked_by_overdue_rental(
        self, client, make_user, make_car, make_rental, user_data, set_status
    ):
        user, car = make_user(), make_car()
        rental = make_rental(user, car)
        set_status("car_rental", rental["id"], "overdue")
        set_status("user", user["id"], "delinquent")
        base = user_data(username=user["username"], email=user["email"])

        resp = client.put(f"{USERS}/{user['id']}", json={**base, "account_status": "active"})

        assert resp.status_code == 422
        assert client.get(f"{USERS}/{user['id']}").get_json()["account_status"] == "delinquent"

    @pytest.mark.xfail(reason="El YAML exige un alquiler overdue para active -> delinquent; "
                              "el negocio dice que el frontend lo solicita directamente.")
    def test_active_to_delinquent_requested_by_frontend(self, client, make_user, user_data):
        user = make_user()
        base = user_data(username=user["username"], email=user["email"])

        resp = client.put(f"{USERS}/{user['id']}", json={**base, "account_status": "delinquent"})

        assert resp.status_code == 200


class TestDelete:
    def test_deletes_user(self, client, make_user):
        user = make_user()

        assert client.delete(f"{USERS}/{user['id']}").status_code == 204
        assert client.get(f"{USERS}/{user['id']}").status_code == 404

    def test_delete_user_with_rentals_fails_and_keeps_user(self, client, make_user, make_car, make_rental):
        user, car = make_user(), make_car()
        make_rental(user, car)

        assert client.delete(f"{USERS}/{user['id']}").status_code == 500
        assert client.get(f"{USERS}/{user['id']}").status_code == 200

    def test_delete_non_existent_user_is_idempotent(self, client):
        assert client.delete(f"{USERS}/{NON_EXISTENT_ID}").status_code == 204
