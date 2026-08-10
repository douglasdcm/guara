# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from pytest import mark, raises

from guara import LOGGER
from guara.policy import TransactionExecutionPolicy
from guara.transaction import AbstractTransaction, Application


class ValidateLocal(AbstractTransaction):
    def do(self):
        raise ValueError

    def undo(self):
        LOGGER.info("rollback!")


def test_transaction_run_automatic_rollback_when_policy_rollback_is_true(caplog):
    t = ValidateLocal
    t.policy = TransactionExecutionPolicy(rollback_on_failure=True)
    with raises(ValueError):
        Application().at(t)
    assert "rollback!" in caplog.text


@mark.parametrize("value", ["invalid", -1, object()])
def test_transactions_returns_none_when_invalid_rollback_value(value):
    t = ValidateLocal
    t.policy = TransactionExecutionPolicy(rollback_on_failure=value)
    with raises(ValueError):
        Application().execute(t)
    assert t.policy.rollback_on_failure is None
