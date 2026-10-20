from unittest.mock import MagicMock

import pytest

from exceptions import BusinessRuleError
from services.enums.statuses import CarStatus
from services.rules import car_rules
from services.state_machine import EFFECTS, GUARDS


def _repo_with_status(status):
    repo = MagicMock()
    repo.get_by_id_for_update.return_value = {"id": 1, "status": status}
    return repo


STATUS_GUARDS = [
    (car_rules.car_is_available, CarStatus.AVAILABLE),
    (car_rules.car_is_reserved, CarStatus.RESERVED),
    (car_rules.car_is_rented, CarStatus.RENTED),
    (car_rules.car_is_in_maintenance, CarStatus.MAINTENANCE),
    (car_rules.car_is_inactive, CarStatus.INACTIVE),
    (car_rules.car_is_sold, CarStatus.SOLD),
]

STATUS_EFFECTS = [
    (car_rules.car_to_available, CarStatus.AVAILABLE),
    (car_rules.car_to_reserved, CarStatus.RESERVED),
    (car_rules.car_to_rented, CarStatus.RENTED),
    (car_rules.car_to_maintenance, CarStatus.MAINTENANCE),
    (car_rules.car_to_inactive, CarStatus.INACTIVE),
    (car_rules.car_to_sold, CarStatus.SOLD),
]


class TestRegistry:
    @pytest.mark.parametrize("name", [
        "car_is_available", "car_is_reserved", "car_is_rented",
        "car_is_in_maintenance", "car_is_inactive", "car_is_sold",
    ])
    def test_guards_registered(self, name):
        assert name in GUARDS

    @pytest.mark.parametrize("name", [
        "car_to_available", "car_to_reserved", "car_to_rented",
        "car_to_maintenance", "car_to_inactive", "car_to_sold",
    ])
    def test_effects_registered(self, name):
        assert name in EFFECTS


class TestCarIdHelper:
    def test_car_entity_uses_current_record_id(self, make_ctx):
        ctx = make_ctx(entity="car", current_record={"id": 7})
        assert car_rules._car_id_helper(ctx) == 7

    def test_other_entity_uses_current_record_car_id(self, make_ctx):
        ctx = make_ctx(entity="car_rental", current_record={"car_id": 5}, data={"car_id": 9})
        assert car_rules._car_id_helper(ctx) == 5

    def test_other_entity_falls_back_to_data(self, make_ctx):
        ctx = make_ctx(entity="car_rental", current_record=None, data={"car_id": 9})
        assert car_rules._car_id_helper(ctx) == 9


class TestStatusGuards:
    @pytest.mark.parametrize("guard_fn, ok_status", STATUS_GUARDS)
    def test_passes_when_status_matches(self, make_ctx, guard_fn, ok_status):
        repo = _repo_with_status(ok_status)
        ctx = make_ctx(entity="car", current_record={"id": 1}, car_repo=repo)

        assert guard_fn(ctx) is None
        repo.get_by_id_for_update.assert_called_once_with(1)

    @pytest.mark.parametrize("guard_fn, ok_status", STATUS_GUARDS)
    def test_raises_when_status_differs(self, make_ctx, guard_fn, ok_status):
        other = next(s for s in CarStatus if s != ok_status)
        ctx = make_ctx(entity="car", current_record={"id": 1}, car_repo=_repo_with_status(other))

        with pytest.raises(BusinessRuleError):
            guard_fn(ctx)

    def test_guard_works_from_car_rental_creation_data(self, make_ctx):
        repo = _repo_with_status(CarStatus.AVAILABLE)
        ctx = make_ctx(entity="car_rental", data={"car_id": 4}, car_repo=repo)

        car_rules.car_is_available(ctx)

        repo.get_by_id_for_update.assert_called_once_with(4)

    def test_guard_works_from_existing_rental(self, make_ctx):
        repo = _repo_with_status(CarStatus.RESERVED)
        ctx = make_ctx(entity="car_rental", current_record={"id": 10, "car_id": 6}, car_repo=repo)

        car_rules.car_is_reserved(ctx)

        repo.get_by_id_for_update.assert_called_once_with(6)


class TestStatusEffects:
    @pytest.mark.parametrize("effect_fn, expected", STATUS_EFFECTS)
    def test_updates_car_status(self, make_ctx, effect_fn, expected):
        repo = MagicMock()
        ctx = make_ctx(entity="car", current_record={"id": 1}, car_repo=repo)

        effect_fn(ctx)

        repo.update_status.assert_called_once_with(1, expected)

    def test_effect_from_rental_targets_rental_car(self, make_ctx):
        repo = MagicMock()
        ctx = make_ctx(entity="car_rental", current_record={"id": 10, "car_id": 6}, car_repo=repo)

        car_rules.car_to_rented(ctx)

        repo.update_status.assert_called_once_with(6, CarStatus.RENTED)
