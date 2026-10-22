from unittest.mock import MagicMock

import pytest

from exceptions import InvalidTransitionError, NotFoundError
from services.car_service import CarService


@pytest.fixture
def repo():
    return MagicMock()


@pytest.fixture
def state_machine():
    return MagicMock()


@pytest.fixture
def service(repo, state_machine, db_manager):
    return CarService(repo, state_machine, db_manager)


class TestReads:
    def test_get_all_cars_delegates_filters(self, service, repo):
        repo.get_all.return_value = [{"id": 1}]

        assert service.get_all_cars({"make": "Toyota"}) == [{"id": 1}]
        repo.get_all.assert_called_once_with({"make": "Toyota"})

    def test_get_car_by_id_delegates(self, service, repo):
        repo.get_by_id.return_value = {"id": 1}

        assert service.get_car_by_id(1) == {"id": 1}
        repo.get_by_id.assert_called_once_with(1)

    def test_get_car_by_id_propagates_not_found(self, service, repo):
        repo.get_by_id.side_effect = NotFoundError("x")
        with pytest.raises(NotFoundError):
            service.get_car_by_id(1)


class TestCreateCar:
    def test_uses_state_machine(self, service, state_machine, car_payload):
        state_machine.create.return_value = {"id": 1}

        assert service.create_car(car_payload) == {"id": 1}
        state_machine.create.assert_called_once_with("car", car_payload)


class TestUpdateCar:
    def test_without_status_only_updates_fields(self, service, repo, state_machine, car_dict, car_payload):
        repo.get_by_id_for_update.return_value = car_dict
        repo.update.return_value = car_dict

        assert service.update_car(1, dict(car_payload)) == car_dict

        state_machine.change_status.assert_not_called()
        repo.update.assert_called_once_with(1, car_payload)

    def test_same_status_does_not_change_status(self, service, repo, state_machine, car_dict, car_payload):
        repo.get_by_id_for_update.return_value = car_dict

        service.update_car(1, {**car_payload, "status": "available"})

        state_machine.change_status.assert_not_called()

    def test_new_status_calls_state_machine(self, service, repo, state_machine, car_dict, car_payload):
        repo.get_by_id_for_update.return_value = car_dict

        service.update_car(1, {**car_payload, "status": "maintenance"})

        state_machine.change_status.assert_called_once_with("car", 1, "maintenance")

    def test_status_is_removed_from_fields_sent_to_repo(self, service, repo, car_dict, car_payload):
        repo.get_by_id_for_update.return_value = car_dict

        service.update_car(1, {**car_payload, "status": "maintenance"})

        assert "status" not in repo.update.call_args.args[1]

    def test_runs_inside_transaction(self, service, repo, db_manager, car_dict, car_payload):
        repo.get_by_id_for_update.return_value = car_dict

        service.update_car(1, dict(car_payload))

        db_manager.transaction.assert_called_once()
        db_manager.transaction.return_value.__enter__.assert_called_once()
        db_manager.transaction.return_value.__exit__.assert_called_once()

    def test_not_found_stops_before_update(self, service, repo, state_machine, car_payload):
        repo.get_by_id_for_update.side_effect = NotFoundError("x")

        with pytest.raises(NotFoundError):
            service.update_car(1, dict(car_payload))

        state_machine.change_status.assert_not_called()
        repo.update.assert_not_called()

    def test_invalid_transition_skips_update(self, service, repo, state_machine, car_dict, car_payload):
        repo.get_by_id_for_update.return_value = car_dict
        state_machine.change_status.side_effect = InvalidTransitionError("x")

        with pytest.raises(InvalidTransitionError):
            service.update_car(1, {**car_payload, "status": "rented"})

        repo.update.assert_not_called()


class TestDeleteCar:
    def test_deletes_and_returns_true(self, service, repo):
        assert service.delete_car(1) is True
        repo.delete.assert_called_once_with(1)
