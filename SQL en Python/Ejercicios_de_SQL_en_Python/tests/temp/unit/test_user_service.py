from unittest.mock import MagicMock

import pytest

from exceptions import InvalidTransitionError, NotFoundError
from services.user_service import UserService


@pytest.fixture
def repo():
    return MagicMock()


@pytest.fixture
def state_machine():
    return MagicMock()


@pytest.fixture
def service(repo, state_machine, db_manager):
    return UserService(repo, state_machine, db_manager)


class TestReads:
    def test_get_all_users_delegates_filters(self, service, repo):
        repo.get_all.return_value = [{"id": 1}]

        assert service.get_all_users({"username": "ana"}) == [{"id": 1}]
        repo.get_all.assert_called_once_with({"username": "ana"})

    def test_get_user_by_id_delegates(self, service, repo):
        repo.get_by_id.return_value = {"id": 1}

        assert service.get_user_by_id(1) == {"id": 1}
        repo.get_by_id.assert_called_once_with(1)

    def test_get_user_by_id_propagates_not_found(self, service, repo):
        repo.get_by_id.side_effect = NotFoundError("x")
        with pytest.raises(NotFoundError):
            service.get_user_by_id(1)


class TestCreateUser:
    def test_uses_state_machine(self, service, state_machine, user_payload):
        state_machine.create.return_value = {"id": 1}

        assert service.create_user(user_payload) == {"id": 1}
        state_machine.create.assert_called_once_with("user", user_payload)


class TestUpdateUser:
    def test_without_status_only_updates_fields(self, service, repo, state_machine, user_dict, user_payload):
        repo.get_by_id_for_update.return_value = user_dict
        repo.update.return_value = user_dict

        assert service.update_user(1, dict(user_payload)) == user_dict

        state_machine.change_status.assert_not_called()
        repo.update.assert_called_once_with(1, user_payload)

    def test_same_status_does_not_change_status(self, service, repo, state_machine, user_dict, user_payload):
        repo.get_by_id_for_update.return_value = user_dict

        service.update_user(1, {**user_payload, "account_status": "active"})

        state_machine.change_status.assert_not_called()

    def test_new_status_calls_state_machine(self, service, repo, state_machine, user_dict, user_payload):
        repo.get_by_id_for_update.return_value = user_dict

        service.update_user(1, {**user_payload, "account_status": "inactive"})

        state_machine.change_status.assert_called_once_with("user", 1, "inactive")

    def test_status_is_removed_from_fields_sent_to_repo(self, service, repo, user_dict, user_payload):
        repo.get_by_id_for_update.return_value = user_dict

        service.update_user(1, {**user_payload, "account_status": "inactive"})

        assert "account_status" not in repo.update.call_args.args[1]

    def test_runs_inside_transaction(self, service, repo, db_manager, user_dict, user_payload):
        repo.get_by_id_for_update.return_value = user_dict

        service.update_user(1, dict(user_payload))

        db_manager.transaction.assert_called_once()
        db_manager.transaction.return_value.__enter__.assert_called_once()
        db_manager.transaction.return_value.__exit__.assert_called_once()

    def test_not_found_stops_before_update(self, service, repo, state_machine, user_payload):
        repo.get_by_id_for_update.side_effect = NotFoundError("x")

        with pytest.raises(NotFoundError):
            service.update_user(1, dict(user_payload))

        state_machine.change_status.assert_not_called()
        repo.update.assert_not_called()

    def test_invalid_transition_skips_update(self, service, repo, state_machine, user_dict, user_payload):
        repo.get_by_id_for_update.return_value = user_dict
        state_machine.change_status.side_effect = InvalidTransitionError("x")

        with pytest.raises(InvalidTransitionError):
            service.update_user(1, {**user_payload, "account_status": "inactive"})

        repo.update.assert_not_called()


class TestDeleteUser:
    def test_deletes_and_returns_true(self, service, repo):
        assert service.delete_user(1) is True
        repo.delete.assert_called_once_with(1)
