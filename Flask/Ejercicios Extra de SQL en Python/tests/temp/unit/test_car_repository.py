import pytest

from exceptions import BusinessRuleError, NotFoundError


class TestFormatRecord:
    def test_maps_columns(self, car_repository, car_row, car_dict):
        assert car_repository._format_record(car_row) == car_dict


class TestResultHelpers:
    def test_first_or_raise_returns_first_formatted(self, car_repository, car_row, car_dict):
        assert car_repository._first_or_raise([car_row], 1) == car_dict

    def test_first_or_raise_raises_when_empty(self, car_repository):
        with pytest.raises(NotFoundError, match="99"):
            car_repository._first_or_raise([], 99)

    def test_first_or_none_returns_none_when_empty(self, car_repository):
        assert car_repository._first_or_none([]) is None

    def test_first_or_none_returns_first_formatted(self, car_repository, car_row, car_dict):
        assert car_repository._first_or_none([car_row]) == car_dict

    def test_format_all_returns_empty_list_when_empty(self, car_repository):
        assert car_repository._format_all([]) == []

    def test_format_all_formats_every_row(self, car_repository, car_row, car_dict):
        assert car_repository._format_all([car_row, car_row]) == [car_dict, car_dict]

    def test_all_or_none_returns_none_when_empty(self, car_repository):
        assert car_repository._all_or_none([]) is None

    def test_all_or_none_formats_every_row(self, car_repository, car_row, car_dict):
        assert car_repository._all_or_none([car_row]) == [car_dict]


class TestGetAll:
    def test_without_filters_has_no_where(self, car_repository, db_manager, car_row):
        db_manager.execute_query.return_value = [car_row]

        car_repository.get_all(None)

        query, params = db_manager.execute_query.call_args.args
        assert "WHERE" not in query
        assert params == ()

    def test_with_filters_builds_parametrized_where(self, car_repository, db_manager, car_row):
        db_manager.execute_query.return_value = [car_row]

        car_repository.get_all({"make": "Toyota", "status": "available"})

        query, params = db_manager.execute_query.call_args.args
        assert "WHERE make = %s AND status = %s" in query
        assert params == ("Toyota", "available")

    def test_invalid_filter_raises_and_skips_query(self, car_repository, db_manager):
        with pytest.raises(BusinessRuleError, match="color"):
            car_repository.get_all({"color": "red"})
        db_manager.execute_query.assert_not_called()

    def test_sql_injection_in_filter_name_is_rejected(self, car_repository, db_manager):
        with pytest.raises(BusinessRuleError):
            car_repository.get_all({"make = make; DROP TABLE x; --": "1"})
        db_manager.execute_query.assert_not_called()

    def test_no_results_returns_empty_list(self, car_repository, db_manager):
        db_manager.execute_query.return_value = []
        assert car_repository.get_all({}) == []

    def test_returns_formatted_list(self, car_repository, db_manager, car_row, car_dict):
        db_manager.execute_query.return_value = [car_row]
        assert car_repository.get_all({}) == [car_dict]


class TestGetById:
    def test_returns_car(self, car_repository, db_manager, car_row, car_dict):
        db_manager.execute_query.return_value = [car_row]

        assert car_repository.get_by_id(1) == car_dict
        assert db_manager.execute_query.call_args.args[1] == (1,)

    def test_not_found(self, car_repository, db_manager):
        db_manager.execute_query.return_value = []
        with pytest.raises(NotFoundError):
            car_repository.get_by_id(1)


class TestGetByIdForUpdate:
    def test_query_locks_row(self, car_repository, db_manager, car_row, car_dict):
        db_manager.execute_query.return_value = [car_row]

        assert car_repository.get_by_id_for_update(1) == car_dict
        assert "FOR UPDATE" in db_manager.execute_query.call_args.args[0]

    def test_not_found(self, car_repository, db_manager):
        db_manager.execute_query.return_value = []
        with pytest.raises(NotFoundError):
            car_repository.get_by_id_for_update(1)


class TestCreate:
    def test_inserts_and_returns_car(self, car_repository, db_manager, car_row, car_dict, car_payload):
        db_manager.execute_query.return_value = [car_row]
        data = {**car_payload, "status": "available"}

        assert car_repository.create(data) == car_dict

        query, params = db_manager.execute_query.call_args.args
        assert query.startswith("INSERT INTO lyfter_car_rental.car")
        assert params == ("Toyota", "Corolla", 2020, "available")

    def test_missing_field_raises_key_error(self, car_repository, car_payload):
        with pytest.raises(KeyError):
            car_repository.create(car_payload)  # sin status


class TestUpdate:
    def test_updates_without_touching_status(self, car_repository, db_manager, car_row, car_dict, car_payload):
        db_manager.execute_query.return_value = [car_row]

        assert car_repository.update(1, car_payload) == car_dict

        query, params = db_manager.execute_query.call_args.args
        assert "status = %s" not in query
        assert params == ("Toyota", "Corolla", 2020, 1)

    def test_missing_field_raises_key_error(self, car_repository):
        with pytest.raises(KeyError):
            car_repository.update(1, {"make": "x"})

    def test_returns_none_when_no_row_updated(self, car_repository, db_manager, car_payload):
        db_manager.execute_query.return_value = []
        assert car_repository.update(1, car_payload) is None


class TestUpdateStatus:
    def test_updates_status(self, car_repository, db_manager, car_row, car_dict):
        db_manager.execute_query.return_value = [car_row]

        assert car_repository.update_status(1, "reserved") == car_dict
        assert db_manager.execute_query.call_args.args[1] == ("reserved", 1)

    def test_returns_none_when_no_row(self, car_repository, db_manager):
        db_manager.execute_query.return_value = []
        assert car_repository.update_status(1, "reserved") is None


class TestDelete:
    def test_executes_delete_with_id(self, car_repository, db_manager):
        car_repository.delete(1)

        query, params = db_manager.execute_query.call_args.args
        assert query.startswith("DELETE FROM lyfter_car_rental.car")
        assert params == (1,)
