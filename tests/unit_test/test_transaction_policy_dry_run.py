# Copyright (C) 2025-2026 Guara - All Rights Reserved
# You may use, distribute and modify this code under the
# terms of the MIT license.
# Visit: https://guara.readthedocs.io/en/latest/


from pytest import mark, raises

from guara.policy import ApplicationExecutionPolicy, TransactionExecutionPolicy
from guara.transaction import AbstractTransaction, Application


class ValidateLocal(AbstractTransaction):
    def do(self):
        raise ValueError


def test_transaction_run_when_policy_dry_run_is_false():
    t = ValidateLocal
    t.execution_policy = TransactionExecutionPolicy(dry_run=False)
    with raises(ValueError):
        Application().at(t)


def test_transaction_doesnt_run_when_policy_dry_run_is_true(caplog):
    t = ValidateLocal
    t.execution_policy = TransactionExecutionPolicy(dry_run=True)
    Application().at(t)
    assert "Dry run" in caplog.text


def test_transaction_dry_run_overrides_application_dry_run():
    t = ValidateLocal
    t.execution_policy = TransactionExecutionPolicy(dry_run=True)
    Application(ApplicationExecutionPolicy(dry_run=False)).at(t)


@mark.parametrize("value", ["invalid", -1, object()])
def test_transactions_returns_none_when_invalid_dry_run_value(value):
    t = ValidateLocal
    t.execution_policy = TransactionExecutionPolicy(dry_run=value)
    with raises(ValueError):
        Application().execute(t)
    assert t.execution_policy.dry_run is None
