import pytest

from exceptions import BusinessRuleError, NotFoundError


@pytest.fixture
def create_payload():
    return {
        "user_id": 3,
        "car_id": 2,
        "rental_date_at": "2025-01-01",
        "return_date_at": "2025-01-05",
        "status": "pending",
    }


class TestFormatRecord:
    def test_maps_columns(self, car_rental_repository, rental_row, rental_dict):
        assert car_rental_repository._format_record(rental_row) == rental_dict


class TestResultHelpers:
    def test_first_or_raise_returns_first_formatted(self, car_rental_repository, rental_row, rental_dict):
        assert car_rental_repository._first_or_raise([rental_row], 1) == rental_dict

    def test_first_or_raise_raises_when_empty(self, car_rental_repository):
        with pytest.raises(NotFoundError, match="99"):
            car_rental_repository._first_or_raise([], 99)

    def test_first_or_none_returns_none_when_empty(self, car_rental_repository):
        assert car_rental_repository._first_or_none([]) is None

    def test_first_or_none_returns_first_formatted(self, car_rental_repository, rental_row, rental_dict):
        assert car_rental_repository._first_or_none([rental_row]) == rental_dict

    def test_format_all_returns_empty_list_when_empty(self, car_rental_repository):
        assert car_rental_repository._format_all([]) == []

    def test_format_all_formats_every_row(self, car_rental_repository, rental_row, rental_dict):
        assert car_rental_repository._format_all([rental_row, rental_row]) == [rental_dict, rental_dict]

    def test_all_or_none_returns_none_when_empty(self, car_rental_repository):
        assert car_rental_repository._all_or_none([]) is None

    def test_all_or_none_formats_every_row(self, car_rental_repository, rental_row, rental_dict):
        assert car_rental_repository._all_or_none([rental_row]) == [rental_dict]


class TestGetAll:
    def test_without_filters_has_no_where(self, car_rental_repository, db_manager, rental_row):
        db_manager.execute_query.return_value = [rental_row]

        car_rental_repository.get_all(None)

        query, params = db_manager.execute_query.call_args.args
        assert "WHERE" not in query
        assert params == ()

    def test_with_filters_builds_parametrized_where(self, car_rental_repository, db_manager, rental_row):
        db_manager.execute_query.return_value = [rental_row]

        car_rental_repository.get_all({"user_id": 3, "status": "pending"})

        query, params = db_manager.execute_query.call_args.args
        assert "WHERE user_id = %s AND status = %s" in query
        assert params == (3, "pending")

    def test_invalid_filter_raises_and_skips_query(self, car_rental_repository, db_manager):
        with pytest.raises(BusinessRuleError, match="color"):
            car_rental_repository.get_all({"color": "red"})
        db_manager.execute_query.assert_not_called()

    def test_sql_injection_in_filter_name_is_rejected(self, car_rental_repository, db_manager):
        with pytest.raises(BusinessRuleError):
            car_rental_repository.get_all({"status = status; DROP TABLE x; --": "1"})
        db_manager.execute_query.assert_not_called()

    def test_no_results_returns_empty_list(self, car_rental_repository, db_manager):
        db_manager.execute_query.return_value = []
        assert car_rental_repository.get_all({}) == []

    def test_returns_formatted_list(self, car_rental_repository, db_manager, rental_row, rental_dict):
        db_manager.execute_query.return_value = [rental_row]
        assert car_rental_repository.get_all({}) == [rental_dict]


class TestGetById:
    def test_returns_rental(self, car_rental_repository, db_manager, rental_row, rental_dict):
        db_manager.execute_query.return_value = [rental_row]

        assert car_rental_repository.get_by_id(1) == rental_dict
        assert db_manager.execute_query.call_args.args[1] == (1,)

    def test_not_found(self, car_rental_repository, db_manager):
        db_manager.execute_query.return_value = []
        with pytest.raises(NotFoundError):
            car_rental_repository.get_by_id(1)


class TestGetByIdForUpdate:
    def test_query_locks_row(self, car_rental_repository, db_manager, rental_row, rental_dict):
        db_manager.execute_query.return_value = [rental_row]

        assert car_rental_repository.get_by_id_for_update(1) == rental_dict
        assert "FOR UPDATE" in db_manager.execute_query.call_args.args[0]

    def test_not_found(self, car_rental_repository, db_manager):
        db_manager.execute_query.return_value = []
        with pytest.raises(NotFoundError):
            car_rental_repository.get_by_id_for_update(1)


class TestGetByUserIdAndRentalStatus:
    def test_returns_list_and_locks(self, car_rental_repository, db_manager, rental_row, rental_dict):
        db_manager.execute_query.return_value = [rental_row]

        result = car_rental_repository.get_by_user_id_and_rental_status(3, "active")

        query, params = db_manager.execute_query.call_args.args
        assert result == [rental_dict]
        assert "FOR UPDATE" in query
        assert params == (3, "active")

    def test_returns_none_when_empty(self, car_rental_repository, db_manager):
        db_manager.execute_query.return_value = []
        assert car_rental_repository.get_by_user_id_and_rental_status(3, "active") is None


class TestGetByUserIdAndMultipleRentalStatus:
    def test_builds_one_placeholder_per_status(self, car_rental_repository, db_manager, rental_row, rental_dict):
        db_manager.execute_query.return_value = [rental_row]

        result = car_rental_repository.get_by_user_id_and_multiple_rental_status(
            3, ["pending", "active", "overdue"]
        )

        query, params = db_manager.execute_query.call_args.args
        assert result == [rental_dict]
        assert "IN (%s,%s,%s)" in query
        assert params == [3, "pending", "active", "overdue"]

    def test_returns_none_when_empty(self, car_rental_repository, db_manager):
        db_manager.execute_query.return_value = []
        assert car_rental_repository.get_by_user_id_and_multiple_rental_status(3, ["pending"]) is None


class TestGetByCarIdAndRentalStatus:
    def test_returns_list_and_locks(self, car_rental_repository, db_manager, rental_row, rental_dict):
        db_manager.execute_query.return_value = [rental_row]

        result = car_rental_repository.get_by_car_id_and_rental_status(2, "active")

        query, params = db_manager.execute_query.call_args.args
        assert result == [rental_dict]
        assert "FOR UPDATE" in query
        assert params == (2, "active")

    def test_returns_none_when_empty(self, car_rental_repository, db_manager):
        db_manager.execute_query.return_value = []
        assert car_rental_repository.get_by_car_id_and_rental_status(2, "active") is None


class TestCreate:
    def test_inserts_and_returns_rental(self, car_rental_repository, db_manager, rental_row, rental_dict, create_payload):
        db_manager.execute_query.return_value = [rental_row]

        assert car_rental_repository.create(create_payload) == rental_dict

        query, params = db_manager.execute_query.call_args.args
        assert query.startswith("INSERT INTO lyfter_car_rental.car_rental")
        assert params == (3, 2, "2025-01-05", "pending")

    def test_missing_field_raises_key_error(self, car_rental_repository, create_payload):
        del create_payload["status"]
        with pytest.raises(KeyError):
            car_rental_repository.create(create_payload)


class TestUpdate:
    def test_only_updates_return_date(self, car_rental_repository, db_manager, rental_row, rental_dict, rental_payload):
        db_manager.execute_query.return_value = [rental_row]

        assert car_rental_repository.update(1, rental_payload) == rental_dict

        query, params = db_manager.execute_query.call_args.args
        assert "SET return_date_at = %s" in query
        assert params == ("2025-01-10", 1)

    def test_missing_field_raises_key_error(self, car_rental_repository):
        with pytest.raises(KeyError):
            car_rental_repository.update(1, {})

    def test_returns_none_when_no_row_updated(self, car_rental_repository, db_manager, rental_payload):
        db_manager.execute_query.return_value = []
        assert car_rental_repository.update(1, rental_payload) is None


class TestUpdateStatus:
    def test_updates_status(self, car_rental_repository, db_manager, rental_row, rental_dict):
        db_manager.execute_query.return_value = [rental_row]

        assert car_rental_repository.update_status(1, "active") == rental_dict
        assert db_manager.execute_query.call_args.args[1] == ("active", 1)

    def test_returns_none_when_no_row(self, car_rental_repository, db_manager):
        db_manager.execute_query.return_value = []
        assert car_rental_repository.update_status(1, "active") is None


class TestDelete:
    def test_executes_delete_with_id(self, car_rental_repository, db_manager):
        car_rental_repository.delete(1)

        query, params = db_manager.execute_query.call_args.args
        assert query.startswith("DELETE FROM lyfter_car_rental.car_rental")
        assert params == (1,)
