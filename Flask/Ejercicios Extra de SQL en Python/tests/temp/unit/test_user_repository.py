import pytest

from exceptions import BusinessRuleError, NotFoundError


class TestFormatRecord:
    def test_maps_columns_and_masks_password(self, user_repository, user_row, user_dict):
        assert user_repository._format_record(user_row) == user_dict


class TestResultHelpers:
    def test_first_or_raise_returns_first_formatted(self, user_repository, user_row, user_dict):
        assert user_repository._first_or_raise([user_row], 1) == user_dict

    def test_first_or_raise_raises_when_empty(self, user_repository):
        with pytest.raises(NotFoundError, match="99"):
            user_repository._first_or_raise([], 99)

    def test_first_or_none_returns_none_when_empty(self, user_repository):
        assert user_repository._first_or_none([]) is None

    def test_first_or_none_returns_first_formatted(self, user_repository, user_row, user_dict):
        assert user_repository._first_or_none([user_row]) == user_dict

    def test_format_all_returns_empty_list_when_empty(self, user_repository):
        assert user_repository._format_all([]) == []

    def test_format_all_formats_every_row(self, user_repository, user_row, user_dict):
        assert user_repository._format_all([user_row, user_row]) == [user_dict, user_dict]

    def test_all_or_none_returns_none_when_empty(self, user_repository):
        assert user_repository._all_or_none([]) is None

    def test_all_or_none_formats_every_row(self, user_repository, user_row, user_dict):
        assert user_repository._all_or_none([user_row]) == [user_dict]


class TestGetAll:
    def test_without_filters_has_no_where(self, user_repository, db_manager, user_row):
        db_manager.execute_query.return_value = [user_row]

        user_repository.get_all()

        query, params = db_manager.execute_query.call_args.args
        assert "WHERE" not in query
        assert params == ()

    def test_with_filters_builds_parametrized_where(self, user_repository, db_manager, user_row):
        db_manager.execute_query.return_value = [user_row]

        user_repository.get_all({"username": "ana", "account_status": "active"})

        query, params = db_manager.execute_query.call_args.args
        assert "WHERE username = %s AND account_status = %s" in query
        assert params == ("ana", "active")

    def test_invalid_filter_raises_and_skips_query(self, user_repository, db_manager):
        with pytest.raises(BusinessRuleError, match="password"):
            user_repository.get_all({"password": "x"})
        db_manager.execute_query.assert_not_called()

    def test_sql_injection_in_filter_name_is_rejected(self, user_repository, db_manager):
        with pytest.raises(BusinessRuleError):
            user_repository.get_all({"name = name; DROP TABLE x; --": "1"})
        db_manager.execute_query.assert_not_called()

    def test_no_results_returns_empty_list(self, user_repository, db_manager):
        db_manager.execute_query.return_value = []
        assert user_repository.get_all() == []

    def test_returns_formatted_list(self, user_repository, db_manager, user_row, user_dict):
        db_manager.execute_query.return_value = [user_row]
        assert user_repository.get_all() == [user_dict]


class TestGetById:
    def test_returns_user(self, user_repository, db_manager, user_row, user_dict):
        db_manager.execute_query.return_value = [user_row]

        assert user_repository.get_by_id(1) == user_dict
        assert db_manager.execute_query.call_args.args[1] == (1,)

    def test_not_found(self, user_repository, db_manager):
        db_manager.execute_query.return_value = []
        with pytest.raises(NotFoundError):
            user_repository.get_by_id(1)


class TestGetByIdForUpdate:
    def test_query_locks_row(self, user_repository, db_manager, user_row, user_dict):
        db_manager.execute_query.return_value = [user_row]

        assert user_repository.get_by_id_for_update(1) == user_dict
        assert "FOR UPDATE" in db_manager.execute_query.call_args.args[0]

    def test_not_found(self, user_repository, db_manager):
        db_manager.execute_query.return_value = []
        with pytest.raises(NotFoundError):
            user_repository.get_by_id_for_update(1)


class TestGetByUsernameOrEmailForUpdate:
    def test_returns_user_when_found(self, user_repository, db_manager, user_row, user_dict):
        db_manager.execute_query.return_value = [user_row]

        result = user_repository.get_by_username_or_email_for_update("ana", "ana@mail.com")

        query, params = db_manager.execute_query.call_args.args
        assert result == user_dict
        assert "FOR UPDATE" in query
        assert params == ("ana", "ana@mail.com")

    def test_returns_none_when_missing(self, user_repository, db_manager):
        db_manager.execute_query.return_value = []
        assert user_repository.get_by_username_or_email_for_update("a", "b") is None


class TestCreate:
    def test_inserts_and_returns_user(self, user_repository, db_manager, user_row, user_dict, user_payload):
        db_manager.execute_query.return_value = [user_row]
        data = {**user_payload, "account_status": "active"}

        assert user_repository.create(data) == user_dict

        query, params = db_manager.execute_query.call_args.args
        assert query.startswith("INSERT INTO lyfter_car_rental.user")
        assert params == ("Ana", "ana@mail.com", "ana", "secret", "1990-01-01", "active")

    def test_missing_field_raises_key_error(self, user_repository, user_payload):
        with pytest.raises(KeyError):
            user_repository.create(user_payload)  # sin account_status


class TestUpdate:
    def test_updates_without_touching_status(self, user_repository, db_manager, user_row, user_dict, user_payload):
        db_manager.execute_query.return_value = [user_row]

        assert user_repository.update(1, user_payload) == user_dict

        query, params = db_manager.execute_query.call_args.args
        assert "account_status = %s" not in query
        assert params == ("Ana", "ana@mail.com", "ana", "secret", "1990-01-01", 1)

    def test_missing_field_raises_key_error(self, user_repository):
        with pytest.raises(KeyError):
            user_repository.update(1, {"name": "x"})

    def test_returns_none_when_no_row_updated(self, user_repository, db_manager, user_payload):
        db_manager.execute_query.return_value = []
        assert user_repository.update(1, user_payload) is None


class TestUpdateStatus:
    def test_updates_status(self, user_repository, db_manager, user_row, user_dict):
        db_manager.execute_query.return_value = [user_row]

        assert user_repository.update_status(1, "inactive") == user_dict
        assert db_manager.execute_query.call_args.args[1] == ("inactive", 1)

    def test_returns_none_when_no_row(self, user_repository, db_manager):
        db_manager.execute_query.return_value = []
        assert user_repository.update_status(1, "inactive") is None


class TestDelete:
    def test_executes_delete_with_id(self, user_repository, db_manager):
        user_repository.delete(1)

        query, params = db_manager.execute_query.call_args.args
        assert query.startswith("DELETE FROM lyfter_car_rental.user")
        assert params == (1,)
