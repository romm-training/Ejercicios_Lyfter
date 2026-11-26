from unittest.mock import MagicMock

import pytest

from exceptions import BusinessRuleError
from services.enums.statuses import UserStatus
from services.rules import user_rules
from services.state_machine import EFFECTS, GUARDS


def _repo_with_status(status):
    repo = MagicMock()
    repo.get_by_id_for_update.return_value = {"id": 1, "account_status": status}
    return repo


class TestRegistry:
    @pytest.mark.parametrize("name", [
        "user_is_active", "user_is_inactive", "user_is_delinquent", "username_and_email_no_exist",
    ])
    def test_guards_registered(self, name):
        assert name in GUARDS

    @pytest.mark.parametrize("name", ["user_to_active", "user_to_inactive", "user_to_delinquent"])
    def test_effects_registered(self, name):
        assert name in EFFECTS


class TestUserIdHelper:
    def test_user_entity_uses_current_record_id(self, make_ctx):
        ctx = make_ctx(entity="user", current_record={"id": 7})
        assert user_rules._user_id_helper(ctx) == 7

    def test_other_entity_uses_current_record_user_id(self, make_ctx):
        ctx = make_ctx(entity="car_rental", current_record={"user_id": 5}, data={"user_id": 9})
        assert user_rules._user_id_helper(ctx) == 5

    def test_other_entity_falls_back_to_data(self, make_ctx):
        ctx = make_ctx(entity="car_rental", current_record=None, data={"user_id": 9})
        assert user_rules._user_id_helper(ctx) == 9


class TestStatusGuards:
    @pytest.mark.parametrize("guard_fn, ok_status", [
        (user_rules.user_is_active, UserStatus.ACTIVE),
        (user_rules.user_is_inactive, UserStatus.INACTIVE),
        (user_rules.user_is_delinquent, UserStatus.DELINQUENT),
    ])
    def test_passes_when_status_matches(self, make_ctx, guard_fn, ok_status):
        repo = _repo_with_status(ok_status)
        ctx = make_ctx(current_record={"id": 1}, user_repo=repo)

        assert guard_fn(ctx) is None
        repo.get_by_id_for_update.assert_called_once_with(1)

    @pytest.mark.parametrize("guard_fn, ok_status", [
        (user_rules.user_is_active, UserStatus.ACTIVE),
        (user_rules.user_is_inactive, UserStatus.INACTIVE),
        (user_rules.user_is_delinquent, UserStatus.DELINQUENT),
    ])
    def test_raises_when_status_differs(self, make_ctx, guard_fn, ok_status):
        other = next(s for s in UserStatus if s != ok_status)
        ctx = make_ctx(current_record={"id": 1}, user_repo=_repo_with_status(other))

        with pytest.raises(BusinessRuleError):
            guard_fn(ctx)

    def test_guard_works_from_car_rental_creation_data(self, make_ctx):
        repo = _repo_with_status(UserStatus.ACTIVE)
        ctx = make_ctx(entity="car_rental", data={"user_id": 4}, user_repo=repo)

        user_rules.user_is_active(ctx)

        repo.get_by_id_for_update.assert_called_once_with(4)


class TestUsernameAndEmailNoExist:
    def test_passes_when_not_taken_on_creation(self, make_ctx, user_payload):
        repo = MagicMock()
        repo.get_by_username_or_email_for_update.return_value = None
        ctx = make_ctx(data=user_payload, user_repo=repo)

        user_rules.username_and_email_no_exist(ctx)

        repo.get_by_username_or_email_for_update.assert_called_once_with("ana", "ana@mail.com")

    def test_raises_when_taken(self, make_ctx, user_payload, user_dict):
        repo = MagicMock()
        repo.get_by_username_or_email_for_update.return_value = user_dict
        ctx = make_ctx(data=user_payload, user_repo=repo)

        with pytest.raises(BusinessRuleError):
            user_rules.username_and_email_no_exist(ctx)

    def test_prefers_current_record_over_data(self, make_ctx, user_payload):
        repo = MagicMock()
        repo.get_by_username_or_email_for_update.return_value = None
        record = {"username": "bob", "email": "bob@mail.com"}
        ctx = make_ctx(current_record=record, data=user_payload, user_repo=repo)

        user_rules.username_and_email_no_exist(ctx)

        repo.get_by_username_or_email_for_update.assert_called_once_with("bob", "bob@mail.com")


class TestStatusEffects:
    @pytest.mark.parametrize("effect_fn, expected", [
        (user_rules.user_to_active, UserStatus.ACTIVE),
        (user_rules.user_to_inactive, UserStatus.INACTIVE),
        (user_rules.user_to_delinquent, UserStatus.DELINQUENT),
    ])
    def test_updates_user_status(self, make_ctx, effect_fn, expected):
        repo = MagicMock()
        ctx = make_ctx(current_record={"id": 1}, user_repo=repo)

        effect_fn(ctx)

        repo.update_status.assert_called_once_with(1, expected)
