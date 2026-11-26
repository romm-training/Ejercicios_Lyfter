from unittest.mock import MagicMock

import pytest

from exceptions import BusinessRuleError
from services.enums.statuses import CarRentalStatus
from services.rules import car_rental_rules as rules
from services.state_machine import EFFECTS, GUARDS


def _repo_with_status(status):
    repo = MagicMock()
    repo.get_by_id_for_update.return_value = {"id": 1, "status": status}
    return repo


STATUS_GUARDS = [
    (rules.rental_is_pending, CarRentalStatus.PENDING),
    (rules.rental_is_active, CarRentalStatus.ACTIVE),
    (rules.rental_is_completed, CarRentalStatus.COMPLETED),
    (rules.rental_is_cancelled, CarRentalStatus.CANCELLED),
    (rules.rental_is_overdue, CarRentalStatus.OVERDUE),
]

STATUS_EFFECTS = [
    (rules.rental_to_pending, CarRentalStatus.PENDING),
    (rules.rental_to_active, CarRentalStatus.ACTIVE),
    (rules.rental_to_completed, CarRentalStatus.COMPLETED),
    (rules.rental_to_cancelled, CarRentalStatus.CANCELLED),
    (rules.rental_to_overdue, CarRentalStatus.OVERDUE),
]


class TestRegistry:
    @pytest.mark.parametrize("name", [
        "rental_is_pending", "rental_is_active", "rental_is_completed",
        "rental_is_cancelled", "rental_is_overdue",
        "user_has_no_active_rentals", "user_has_overdue_rentals",
        "user_has_no_overdue_rentals", "user_has_no_active_pending_overdue_rentals",
        "car_has_no_active_rentals",
    ])
    def test_guards_registered(self, name):
        assert name in GUARDS

    @pytest.mark.parametrize("name", [
        "rental_to_pending", "rental_to_active", "rental_to_completed",
        "rental_to_cancelled", "rental_to_overdue",
    ])
    def test_effects_registered(self, name):
        assert name in EFFECTS


class TestStatusGuards:
    @pytest.mark.parametrize("guard_fn, ok_status", STATUS_GUARDS)
    def test_passes_when_status_matches(self, make_ctx, guard_fn, ok_status):
        repo = _repo_with_status(ok_status)
        ctx = make_ctx(entity="car_rental", current_record={"id": 1}, rental_repo=repo)

        assert guard_fn(ctx) is None
        repo.get_by_id_for_update.assert_called_once_with(1)

    @pytest.mark.parametrize("guard_fn, ok_status", STATUS_GUARDS)
    def test_raises_when_status_differs(self, make_ctx, guard_fn, ok_status):
        other = next(s for s in CarRentalStatus if s != ok_status)
        ctx = make_ctx(entity="car_rental", current_record={"id": 1}, rental_repo=_repo_with_status(other))

        with pytest.raises(BusinessRuleError):
            guard_fn(ctx)


class TestUserRentalGuards:
    """Estos guards se ejecutan sobre un usuario: current_record es el usuario."""

    def test_no_active_rentals_raises_when_user_has_active(self, make_ctx):
        repo = MagicMock()
        repo.get_by_user_id_and_rental_status.return_value = [{"id": 1}]
        ctx = make_ctx(entity="user", current_record={"id": 3}, rental_repo=repo)

        with pytest.raises(BusinessRuleError):
            rules.user_has_no_active_rentals(ctx)
        repo.get_by_user_id_and_rental_status.assert_called_once_with(3, CarRentalStatus.ACTIVE)

    def test_no_active_rentals_passes_when_user_has_none(self, make_ctx):
        repo = MagicMock()
        repo.get_by_user_id_and_rental_status.return_value = None
        ctx = make_ctx(entity="user", current_record={"id": 3}, rental_repo=repo)

        assert rules.user_has_no_active_rentals(ctx) is None

    def test_has_overdue_rentals_raises_when_user_has_none(self, make_ctx):
        repo = MagicMock()
        repo.get_by_user_id_and_rental_status.return_value = None
        ctx = make_ctx(entity="user", current_record={"id": 3}, rental_repo=repo)

        with pytest.raises(BusinessRuleError):
            rules.user_has_overdue_rentals(ctx)
        repo.get_by_user_id_and_rental_status.assert_called_once_with(3, CarRentalStatus.OVERDUE)

    def test_has_overdue_rentals_passes_when_user_has_overdue(self, make_ctx):
        repo = MagicMock()
        repo.get_by_user_id_and_rental_status.return_value = [{"id": 1}]
        ctx = make_ctx(entity="user", current_record={"id": 3}, rental_repo=repo)

        assert rules.user_has_overdue_rentals(ctx) is None

    def test_no_overdue_rentals_raises_when_user_has_overdue(self, make_ctx):
        repo = MagicMock()
        repo.get_by_user_id_and_rental_status.return_value = [{"id": 1}]
        ctx = make_ctx(entity="user", current_record={"id": 3}, rental_repo=repo)

        with pytest.raises(BusinessRuleError):
            rules.user_has_no_overdue_rentals(ctx)
        repo.get_by_user_id_and_rental_status.assert_called_once_with(3, CarRentalStatus.OVERDUE)

    def test_no_overdue_rentals_passes_when_none(self, make_ctx):
        repo = MagicMock()
        repo.get_by_user_id_and_rental_status.return_value = None
        ctx = make_ctx(entity="user", current_record={"id": 3}, rental_repo=repo)

        assert rules.user_has_no_overdue_rentals(ctx) is None

    def test_no_open_rentals_passes_when_none(self, make_ctx):
        repo = MagicMock()
        repo.get_by_user_id_and_multiple_rental_status.return_value = None
        ctx = make_ctx(entity="user", current_record={"id": 3}, rental_repo=repo)

        assert rules.user_has_no_active_pending_overdue_rentals(ctx) is None
        repo.get_by_user_id_and_multiple_rental_status.assert_called_once_with(
            3, [CarRentalStatus.ACTIVE, CarRentalStatus.PENDING, CarRentalStatus.OVERDUE]
        )

    def test_no_open_rentals_raises_when_any(self, make_ctx):
        repo = MagicMock()
        repo.get_by_user_id_and_multiple_rental_status.return_value = [{"id": 1}]
        ctx = make_ctx(entity="user", current_record={"id": 3}, rental_repo=repo)

        with pytest.raises(BusinessRuleError):
            rules.user_has_no_active_pending_overdue_rentals(ctx)


class TestCarHasNoActiveRentals:
    def test_passes_when_none(self, make_ctx):
        repo = MagicMock()
        repo.get_by_car_id_and_rental_status.return_value = None
        ctx = make_ctx(entity="car", current_record={"id": 2}, rental_repo=repo)

        assert rules.car_has_no_active_rentals(ctx) is None
        repo.get_by_car_id_and_rental_status.assert_called_once_with(2, CarRentalStatus.ACTIVE)

    def test_raises_when_car_has_active_rental(self, make_ctx):
        repo = MagicMock()
        repo.get_by_car_id_and_rental_status.return_value = [{"id": 1}]
        ctx = make_ctx(entity="car", current_record={"id": 2}, rental_repo=repo)

        with pytest.raises(BusinessRuleError):
            rules.car_has_no_active_rentals(ctx)


class TestStatusEffects:
    @pytest.mark.parametrize("effect_fn, expected", STATUS_EFFECTS)
    def test_updates_rental_status(self, make_ctx, effect_fn, expected):
        repo = MagicMock()
        ctx = make_ctx(entity="car_rental", current_record={"id": 1}, rental_repo=repo)

        effect_fn(ctx)

        repo.update_status.assert_called_once_with(1, expected)
